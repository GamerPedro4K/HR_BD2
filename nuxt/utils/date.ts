export function formatDate(
    dateString: string,
    locale: string = "pt-PT",
    options: Intl.DateTimeFormatOptions = {}
  ): string {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString(locale, {
        year: "numeric",
        month: "long",
        day: "numeric",
        ...options,
      });
    } catch (error) {
      console.error("Invalid date:", dateString);
      return "Data inválida";
    }
  }
  
  export function formatTime(
    dateString: string,
    locale: string = "pt-PT",
    options: Intl.DateTimeFormatOptions = {}
  ): string {
    try {
      const date = new Date(dateString);
      return date.toLocaleTimeString(locale, {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        ...options,
      });
    } catch (error) {
      console.error("Invalid time:", dateString);
      return "Hora inválida";
    }
  }
  
  export function formatDateTime(
    dateString: string,
    locale: string = "pt-PT",
    dateOptions: Intl.DateTimeFormatOptions = {},
    timeOptions: Intl.DateTimeFormatOptions = {}
  ): string {
    try {
      const date = new Date(dateString);
      const formattedDate = date.toLocaleDateString(locale, {
        year: "numeric",
        month: "long",
        day: "numeric",
        ...dateOptions,
      });
      const formattedTime = date.toLocaleTimeString(locale, {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        ...timeOptions,
      });
      return `${formattedDate} às ${formattedTime}`;
    } catch (error) {
      console.error("Invalid date-time:", dateString);
      return "Data/Hora inválida";
    }
  }

  export function formatDateRequest(date: Date | undefined) {
    return date ? date.toISOString().split('T')[0] : new Date().toISOString().split('T')[0]; // Convert to YYYY-MM-DD
  };
  