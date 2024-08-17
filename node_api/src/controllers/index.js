import express from "express";
import HealthCheckController from "./HealthCheckController.js";
import TodosController from "./TodosController.js";

const router = express.Router();

router.use("/health-check-controller", HealthCheckController);
router.use("/todos-controller", TodosController);

export default router;
