import { getPostService } from "../services/getPostService/index.js";
import express from "express";
const router = express.Router();
import { getPostsService } from "../services/getPostsService/index.js";

router.get("/posts", async (req, res) => {
  const { params, body, query } = req;
  try {
    let finalData = {};
    const getPostsServiceData = await getPostsService({ params, body, query });
    finalData["getPostsService"] = getPostsServiceData;

    res.json(finalData);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get("/:id", async (req, res) => {
  const { params, body, query } = req;
  try {
    let finalData = {};
    const getPostServiceData = await getPostService({ params, body, query });
    finalData["getPostService"] = getPostServiceData;

    res.json(finalData);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
