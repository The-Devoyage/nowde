export const health = async () => {
  const response = await fetch("/health", {
    method: "get",
  });
  return await response.json();
};
