import { defineNuxtPlugin } from '#app';

export default defineNuxtPlugin((nuxtApp) => {
  const { isLoading, start, finish, clear } = useLoadingIndicator({
    duration: 2000,
    throttle: 200,
    estimatedProgress: (duration, elapsed) =>
      (2 / Math.PI * 100) * Math.atan((elapsed / duration) * 100 / 50),
  });

  nuxtApp.provide('loadingIndicator', {
    isLoading,
    start,
    finish,
    clear,
  });
});
