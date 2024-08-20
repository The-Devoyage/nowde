export const getPostsService = async ({ params, body, query }) => {
  const search_query_string = new URLSearchParams(query).toString();

  try {
    const response = await fetch(
      `https://jsonplaceholder.typicode.com/posts` + search_query_string,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      },
    );

    return await response.json();
  } catch (error) {
    console.error(error);
    return { error: error.message };
  }
};
