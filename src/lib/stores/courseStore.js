import { writable } from 'svelte/store';

export const courses = writable([]);
export const currentPosition = writable(1);
export const completedLevels = writable(new Set([1]));