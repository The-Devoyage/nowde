import express from "express";
import todosController from "./todosController.js";
import postsController from "./postsController.js";

const router = express.Router();

router.use("/todo", todosController);
router.use("/post", postsController);

export default router;
