export const TodosService = async () => {
  const response = await fetch("/todos/:id", {
    method: "GET",
  });
  return await response.json();
};
