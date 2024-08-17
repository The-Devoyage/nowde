import express from "express";
const router = express.Router();
import { TodosService } from "../services/TodosService/index.js";

router.get("/", async (req, res) => {
  try {
    let finalData = {};
    const TodosServiceData = await TodosService();
    finalData["TodosService"] = TodosServiceData;

    res.json(finalData);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
