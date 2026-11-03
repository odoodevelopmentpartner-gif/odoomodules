/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";

/**
 * POS Auto Lock (my_pos_lock)
 *
 * pos_auto_lock_use_common = true  → always use config.pos_auto_lock_timeout
 * pos_auto_lock_use_common = false → use employee.pos_auto_lock_timeout if > 0,
 *                                    else fallback to config.pos_auto_lock_timeout
 */
const ACTIVITY_EVENTS = ["mousemove", "mousedown", "keydown", "touchstart", "click", "scroll"];

patch(PosStore.prototype, {
    async setup(...args) {
        await super.setup(...args);
        this._myPosLockTimer = null;
        this._myPosLockBoundOnActivity = null;
        this._myPosLockStarted = false;
    },

    async afterProcessServerData(...args) {
        const result = await super.afterProcessServerData(...args);
        try {
            this._myPosLockEnsureWatcher();
        } catch (e) {
            console.warn("[my_pos_lock] watcher start failed:", e);
        }
        return result;
    },

    setCashier(employee) {
        const result = super.setCashier(...arguments);
        try {
            this._myPosLockResetTimer();
        } catch (e) {
            /* ignore during early init */
        }
        return result;
    },

    resetCashier() {
        const result = super.resetCashier(...arguments);
        try {
            this._myPosLockResetTimer();
        } catch (e) {
            /* ignore */
        }
        return result;
    },

    _myPosLockIsEnabled() {
        const cfg = this.config;
        return Boolean(cfg && cfg.module_pos_hr && cfg.pos_auto_lock);
    },

    /**
     * Effective timeout in seconds.
     */
    _myPosLockEffectiveTimeoutSec() {
        const cfg = this.config;
        const common = Math.max(0, Number(cfg?.pos_auto_lock_timeout) || 0);

        // Common mode: one timeout for everyone
        if (cfg?.pos_auto_lock_use_common) {
            return Math.max(10, common || 60);
        }

        // Separate mode: employee override, else common fallback
        let employeeTimeout = 0;
        try {
            const cashier =
                this.accessRight?.loggedCashier ||
                this.accessRight?.cashier ||
                null;
            const raw = cashier ? cashier.pos_auto_lock_timeout : 0;
            if (Number(raw) > 0) {
                employeeTimeout = Number(raw);
            }
        } catch {
            /* ignore */
        }
        const seconds = employeeTimeout > 0 ? employeeTimeout : common;
        return Math.max(10, seconds || 60);
    },

    _myPosLockIsLockedScreen() {
        try {
            const screen = this.router?.currentScreen?.();
            return screen === "LoginScreen" || screen === "SaverScreen";
        } catch {
            return false;
        }
    },

    _myPosLockEnsureWatcher() {
        if (this._myPosLockStarted || !this._myPosLockIsEnabled()) {
            return;
        }
        this._myPosLockStarted = true;
        this._myPosLockBoundOnActivity = () => this._myPosLockOnActivity();
        for (const evt of ACTIVITY_EVENTS) {
            window.addEventListener(evt, this._myPosLockBoundOnActivity, { passive: true });
        }
        this._myPosLockResetTimer();
    },

    _myPosLockOnActivity() {
        if (!this._myPosLockIsEnabled() || this._myPosLockIsLockedScreen()) {
            return;
        }
        this._myPosLockResetTimer();
    },

    _myPosLockResetTimer() {
        if (this._myPosLockTimer) {
            clearTimeout(this._myPosLockTimer);
            this._myPosLockTimer = null;
        }
        if (!this._myPosLockIsEnabled() || this._myPosLockIsLockedScreen()) {
            return;
        }
        const hasCashier = Boolean(
            this.accessRight?.loggedCashier || this.accessRight?.cashier
        );
        if (!hasCashier) {
            return;
        }
        const ms = this._myPosLockEffectiveTimeoutSec() * 1000;
        this._myPosLockTimer = setTimeout(() => this._myPosLockDoLock(), ms);
    },

    _myPosLockDoLock() {
        if (!this._myPosLockIsEnabled() || this._myPosLockIsLockedScreen()) {
            return;
        }
        try {
            this.login = true;
            if (typeof this.showLoginScreen === "function") {
                this.showLoginScreen();
            } else {
                this.resetCashier();
                this.navigate("LoginScreen");
                this.dialog?.closeAll?.();
            }
        } catch (e) {
            console.warn("[my_pos_lock] lock failed:", e);
        }
        this._myPosLockResetTimer();
    },
});
