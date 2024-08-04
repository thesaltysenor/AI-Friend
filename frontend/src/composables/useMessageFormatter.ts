export function useMessageFormatter() {
  function formatMessage(content: string): string {
    let formattedContent = content.replace(/As an AI assistant,?/gi, '');
    formattedContent = formattedContent.replace(/My role is to assist you,?/gi, '');
    formattedContent = formattedContent.replace(/\n\n/g, '</p><p>');
    return `<p>${formattedContent}</p>`;
  }

  return { formatMessage };
}