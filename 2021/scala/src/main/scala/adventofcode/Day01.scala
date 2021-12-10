package adventofcode

import scala.util.{Failure, Success, Try}

object Day01Part1 {
  def secondIsGreater(pairing: Seq[Int]): Boolean = { pairing(1) > pairing(0) }

  def findIncreasingDepths(lines: Seq[String]): Int = {
    var totalIncreases = 0
    var previousDepth = lines(0).toInt

    for (depth <- lines.drop(1).map(_.toInt).toSeq) {
      if (depth > previousDepth) then totalIncreases += 1
      previousDepth = depth
    }

    totalIncreases
  }

  def functionalFindIncreasingDepths(lines: Seq[String]): Int = {
    lines
      .sliding(2)
      .toSeq
      .map(pairing => secondIsGreater(pairing.map(_.toInt).toSeq))
      .count(_ == true)
  }
}

object Day01Part2 {
  def produceWindows(windowSize: Int, overlap: Int = 1, items: Seq[Int]): Seq[Seq[Int]] = {
    items.sliding(windowSize, overlap).toSeq
  }

  def findIncreasingWindowDepths(lines: Seq[String]): Int = {
    val windowSums =
      produceWindows(3, 1, lines.map(_.toInt).toSeq).map(pairing => pairing.sum).map(_.toString)
    Day01Part1.findIncreasingDepths(windowSums)
  }
}

object Day01 {
  def main(args: Array[String]): Unit = {
    Runner.solve(
      args,
      1,
      Day01Part1.functionalFindIncreasingDepths,
      Day01Part2.findIncreasingWindowDepths,
    )
  }
}
