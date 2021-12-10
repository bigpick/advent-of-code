package adventofcode

import scala.util.{Failure, Success, Try}

object Day02Part1 {
  def handleMovement(x_y_accumulator: (Int, Int), next: String) = {
    next.split(" ").toSeq match {
      case "up" +: movement +: _ => (x_y_accumulator._1, x_y_accumulator._2 - movement.toInt)
      case "down" +: movement +: _ => (x_y_accumulator._1, x_y_accumulator._2 + movement.toInt)
      case "forward" +: movement +: _ =>
        (x_y_accumulator._1 + movement.toInt, x_y_accumulator._2)
    }
  }
  def handleMovementCommands(commands: Seq[String]): Int = {
    val coords = commands.foldLeft((0, 0))(handleMovement)
    coords._1 * coords._2
  }
}
object Day02Part2 {
  def handleMovement(x_y_aim: (Int, Int, Int), next: String) = {
    val (x, y, aim) = x_y_aim
    next.split(" ").toSeq match {
      case "up" +: movement +: _ => (x, y, aim - movement.toInt)
      case "down" +: movement +: _ => (x, y, aim + movement.toInt)
      case "forward" +: movement +: _ =>
        (x + movement.toInt, y + (aim * movement.toInt), aim)
    }
  }
  def handleMovementCommands(commands: Seq[String]): Int = {
    val coords = commands.foldLeft((0, 0, 0))(handleMovement)
    coords._1 * coords._2
  }
}

object Day02 {
  def main(args: Array[String]): Unit = {
    Runner.solve(
      args,
      2,
      Day02Part1.handleMovementCommands,
      Day02Part2.handleMovementCommands,
    )
  }
}
