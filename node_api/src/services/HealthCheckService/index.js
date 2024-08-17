export const HealthCheckService = async () => {
  const response = await fetch("/health", {
    method: "GET",
  });
  return await response.json();
};
