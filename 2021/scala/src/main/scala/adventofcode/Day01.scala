package adventofcode

import scala.util.{Try, Success, Failure}

object Day01Part1 {
  def secondIsGreater(pairing: Seq[Int]): Boolean = {
    pairing(1) > pairing(0)
  }

  def findIncreasingDepths(lines: Seq[Int]): Int = {
    var totalIncreases = 0
    var previousDepth = lines(0)

    for (depth <- lines.drop(1)) {
      if (depth > previousDepth) then totalIncreases += 1
      previousDepth = depth
    }

    totalIncreases
  }

  def functionalFindIncreasingDepths(lines: Seq[Int]): Int = {
    lines
      .sliding(2)
      .toSeq
      .map(pairing => secondIsGreater(pairing))
      .count(_ == true)
  }
}

object Day01Part2 {
  def produceWindows(
      windowSize: Int,
      overlap: Int = 1,
      items: Seq[Int]
  ): Seq[Seq[Int]] = {
    items.sliding(windowSize, overlap).toSeq
  }
}

object Day01 {
  def main(args: Array[String]): Unit = {
    import AOCCliParser.parseCli
    import FileParser.readFile

    val config = parseCli(args)
    val cliArgs = config match {
      case Success(conf) => conf
      case Failure(e)    => throw e
    }

    val challTxt = readFile(cliArgs.challInput)
    challTxt match {
      case Success(lines) =>
        val intChallTxt = lines.map(entry => entry.toInt)
        // Part 1
        val increases = Day01Part1.findIncreasingDepths(intChallTxt)
        val increasesFunctional =
          Day01Part1.functionalFindIncreasingDepths(intChallTxt)
        println(s"Day 1 Part 1: $increases.")

        // Part 2
        val windowSums = Day01Part2
          .produceWindows(3, 1, intChallTxt)
          .map(pairing => pairing.sum)
        val windowedIncreases = Day01Part1.findIncreasingDepths(windowSums)
        println(s"Day 1 Part 2: $windowedIncreases.")

      case _ => ()
    }
  }
}
