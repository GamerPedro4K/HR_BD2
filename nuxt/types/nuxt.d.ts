import { ToastServiceMethods } from 'primevue/usetoast';
import { Ref } from 'vue';

declare module '#app' {
  interface NuxtApp {
    $toast: ToastServiceMethods;
    $loadingIndicator: {
      isLoading: Ref<boolean>;
      start: () => void;
      finish: (options?: { error?: boolean }) => void;
      clear: () => void;
    };
  }
}

declare module 'vue' {
  interface ComponentCustomProperties {
    $toast: ToastServiceMethods;
    $loadingIndicator: {
      isLoading: Ref<boolean>;
      start: () => void;
      finish: (options?: { error?: boolean }) => void;
      clear: () => void;
    };
  }
}

export {};
