import { getTodoService } from "../services/getTodoService/index.js";
import express from "express";
const router = express.Router();
import { getTodosService } from "../services/getTodosService/index.js";

router.get("/todos", async (req, res) => {
  const { params, body, query } = req;
  try {
    let finalData = {};
    const getTodosServiceData = await getTodosService({ params, body, query });
    finalData["getTodosService"] = getTodosServiceData;

    res.json(finalData);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get("/:id", async (req, res) => {
  const { params, body, query } = req;
  try {
    let finalData = {};
    const getTodoServiceData = await getTodoService({ params, body, query });
    finalData["getTodoService"] = getTodoServiceData;

    res.json(finalData);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
