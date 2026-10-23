/**
 * 
 * @param {string} inputText 
 * @param {number} defaultValue 
 * @returns {number}
 */
export function toNumberOrDefault(inputText, defaultValue) {
    if (inputText === null || inputText === undefined) {
        return defaultValue;
    }

    if (typeof inputText === 'string' && inputText.trim() === '') {
        return defaultValue;
    }

    let input = Number(inputText);
    let result = Number.isFinite(input) ? input : defaultValue;
    return result;
};

/**
 * 
 * @param {*} value 
 * @returns {boolean}
 * @example
 * coerceToBoolean(true) => true
 * coerceToBoolean(1) => true
 * coerceToBoolean("true") => true
 * coerceToBoolean("1") => true
 * coerceToBoolean(false) => false
 * coerceToBoolean(0) => false
 * coerceToBoolean("false") => false
 * coerceToBoolean("0") => false
 * coerceToBoolean("") => false
 * coerceToBoolean("any other string") => true
 */
export function coerceToBoolean(value) {
    if (typeof value === 'boolean') {
        return value;
    }
    if (typeof value === 'number') {
        return value !== 0;
    }
    if (typeof value === 'string') {
        const normalized = value.trim().toLowerCase();
        if (normalized === 'true' || normalized === '1') {
            return true;
        }
        if (normalized === 'false' || normalized === '0' || normalized === '') {
            return false;
        }
    }
    return Boolean(value);
}

/**
 * Normalize RWS shared-data payloads to a fixed-length boolean array.
 * Supports arrays, JSON strings, scalars, and sparse/object-like inputs.
 *
 * @param {*} input
 * @param {number} length
 * @returns {boolean[]}
 * @example
 * normalizeSharedBooleanArray([1, 0, true], 4)
 * // => [true, false, true, false]
 *
 * @example
 * normalizeSharedBooleanArray("[\"true\",\"0\",1,false]", 4)
 * // => [true, false, true, false]
 *
 * @example
 * normalizeSharedBooleanArray(true, 4)
 * // => [true, true, true, true]
 *
 * @example
 * normalizeSharedBooleanArray({ 0: 1, 2: "true" }, 4)
 * // => [true, false, true, false]
 */
export function normalizeSharedBooleanArray(input, length) {
    const targetLength = Number.isInteger(length) && length > 0 ? length : 0;
    const normalized = Array.from({ length: targetLength }, () => false);

    let source = input;
    if (typeof source === 'string') {
        try {
            source = JSON.parse(source);
        } catch {
            source = input;
        }
    }

    if (Array.isArray(source)) {
        for (let i = 0; i < targetLength; i++) {
            normalized[i] = coerceToBoolean(source[i]);
        }
        return normalized;
    }

    if (source && typeof source === 'object') {
        for (let i = 0; i < targetLength; i++) {
            normalized[i] = coerceToBoolean(source[i]);
        }
        return normalized;
    }

    const scalar = coerceToBoolean(source);
    for (let i = 0; i < targetLength; i++) {
        normalized[i] = scalar;
    }
    return normalized;
}

export function toRoundedNumber(value, decimals, fallback = 0) {
    const numericValue = Number(value);
    if (!Number.isFinite(numericValue)) {
        return fallback;
    }
    return Number(numericValue.toFixed(decimals));
}

export function toScaledRoundedNumber(value, scale, decimals, fallback = 0) {
    const numericValue = Number(value);
    if (!Number.isFinite(numericValue)) {
        return fallback;
    }
    return Number((numericValue * scale).toFixed(decimals));
}

export function isFiniteInRange(value, min, max) {
    const numericValue = Number(value);
    return Number.isFinite(numericValue) && numericValue >= min && numericValue <= max;
}

export function toRoundedText(value, decimals, fallback = "") {
    const numericValue = Number(value);
    if (!Number.isFinite(numericValue)) {
        return fallback;
    }
    return numericValue.toFixed(decimals);
}