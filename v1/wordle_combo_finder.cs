using System;
using System.Collections.Generic;
using System.Linq;

class Program
{
    private static readonly string[] WORD_LIST = {
        "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult", "after", "again",
        "agent", "agree", "ahead", "alarm", "album", "alert", "align", "alike", "alive", "allow",
        "alone", "along", "alter", "amber", "amend", "among", "ample", "angel", "anger", "angle",
        "angry", "apart", "apple", "apply", "arena", "argue", "arise", "armor", "army", "around",
        "arrow", "aside", "asset", "audio", "audit", "avoid", "awake", "award", "aware", "badly",
        "baker", "bases", "basic", "basis", "beach", "began", "begin", "being", "below", "bench",
        "billy", "birth", "black", "blade", "blame", "blank", "blast", "bleed", "bless", "blind",
        "block", "blood", "bloom", "blown", "board", "boast", "bonus", "boost", "booth", "bound",
        "brain", "brand", "brass", "brave", "bread", "break", "breed", "brief", "bring", "broad",
        "broke", "brown", "build", "built", "burst", "buyer", "cable", "calif", "candy", "carry",
        "catch", "cause", "chain", "chair", "chaos", "charm", "chart", "chase", "cheap", "check",
        "chess", "chest", "chief", "child", "china", "chose", "civil", "claim", "class", "clean",
        "clear", "click", "cliff", "climb", "clock", "close", "cloth", "cloud", "coach", "coast",
        "could", "count", "court", "cover", "crack", "craft", "crane", "crash", "crazy", "cream",
        "crime", "cross", "crowd", "crown", "crude", "curve", "cycle", "daily", "dance", "dated",
        "dealt", "death", "debut", "delay", "depth", "doing", "doubt", "dozen", "draft", "drama",
        "drank", "drawn", "dream", "dress", "dried", "drill", "drink", "drive", "drove", "dying",
        "eager", "eagle", "early", "earth", "eight", "elect", "elite", "empty", "enemy", "enjoy",
        "enter", "entry", "equal", "error", "event", "every", "exact", "exist", "extra", "faith",
        "false", "fault", "fiber", "field", "fifth", "fifty", "fight", "final", "first", "fixed",
        "flash", "fleet", "flesh", "flight", "floor", "fluid", "focus", "force", "forth", "forty",
        "forum", "found", "frame", "frank", "fraud", "fresh", "front", "fruit", "fully", "funny",
        "giant", "given", "glass", "globe", "glory", "going", "grace", "grade", "grain", "grand",
        "grant", "graph", "grasp", "grass", "grave", "great", "green", "greet", "grief", "gross",
        "group", "grown", "guard", "guess", "guest", "guide", "guild", "guilt", "happy", "harry",
        "harsh", "haste", "heart", "heavy", "hence", "henry", "horse", "hotel", "house", "human",
        "ideal", "image", "imply", "index", "inner", "input", "issue", "japan", "jimmy", "jones",
        "judge", "known", "label", "large", "laser", "later", "laugh", "layer", "learn", "lease",
        "least", "leave", "legal", "lemon", "level", "lewis", "light", "limit", "links", "lives",
        "local", "logic", "loose", "lower", "lucky", "lunch", "lying", "magic", "major", "maker",
        "march", "maria", "match", "maybe", "mayor", "meant", "media", "metal", "might", "minor",
        "minus", "mixed", "model", "money", "month", "moral", "motor", "mount", "mouse", "mouth",
        "movie", "music", "needs", "never", "newly", "night", "noise", "north", "noted", "novel",
        "nurse", "occur", "ocean", "offer", "often", "order", "other", "ought", "outer", "owned",
        "owner", "paint", "panel", "panic", "paper", "party", "peace", "peter", "phase", "phone",
        "photo", "piece", "pilot", "pitch", "place", "plain", "plane", "plant", "plate", "plaza",
        "point", "poker", "polar", "pound", "power", "press", "price", "pride", "prime", "print",
        "prior", "prize", "proof", "proud", "prove", "queen", "query", "quest", "queue", "quick",
        "quiet", "quite", "radio", "raise", "range", "rapid", "ratio", "reach", "ready", "refer",
        "reign", "relax", "reply", "rider", "ridge", "rifle", "right", "rigid", "risky", "rival",
        "river", "robin", "rocky", "roman", "rough", "round", "route", "royal", "rural", "scale",
        "scene", "scope", "score", "sense", "serve", "seven", "shall", "shape", "share", "sharp",
        "sheet", "shelf", "shell", "shift", "shine", "shirt", "shock", "shoot", "shore", "short",
        "shown", "sight", "since", "sixth", "sixty", "sized", "skill", "sleep", "slide", "small",
        "smart", "smile", "smith", "smoke", "solid", "solve", "sorry", "sound", "south", "space",
        "spare", "speak", "speed", "spend", "spent", "split", "spoke", "sport", "staff", "stage",
        "stake", "stand", "start", "state", "steam", "steel", "steep", "steer", "steve", "stick",
        "still", "stock", "stone", "stood", "store", "storm", "story", "strip", "stuck", "study",
        "stuff", "style", "sugar", "suite", "sunny", "super", "surge", "sweet", "swift", "swing",
        "sword", "table", "taken", "taste", "taxes", "teach", "terry", "texas", "thank", "theft",
        "their", "theme", "there", "these", "thick", "thing", "think", "third", "those", "three",
        "threw", "throw", "thumb", "tiger", "tight", "timer", "title", "today", "topic", "total",
        "touch", "tough", "tower", "track", "trade", "trail", "train", "trait", "treat", "trend",
        "trial", "tribe", "trick", "tried", "troop", "truck", "truly", "trump", "trust", "truth",
        "twice", "uncle", "under", "undue", "union", "unity", "until", "upper", "upset", "urban",
        "usage", "usual", "valid", "value", "video", "virus", "visit", "vital", "vocal", "voice",
        "waste", "watch", "water", "wheel", "where", "which", "while", "white", "whole", "whose",
        "woman", "women", "world", "worry", "worse", "worst", "worth", "would", "wound", "write",
        "wrong", "wrote", "yield", "young", "yours", "youth", "zones"
    };

    private static (bool isValid, string error) ValidateGuess(string guess, string feedback)
    {
        if (guess.Length != 5 || !guess.All(char.IsLetter))
        {
            return (false, "Guess must be a 5-letter word containing only letters.");
        }
        if (feedback.Length != 5 || !feedback.ToUpper().All(c => c == 'G' || c == 'Y' || c == 'R'))
        {
            return (false, "Feedback must be 5 characters, each 'G' (green), 'Y' (yellow), or 'R' (red).");
        }
        return (true, "");
    }

    private static bool IsValidWord(string word, string guess, string feedback)
    {
        guess = guess.ToLower();
        word = word.ToLower();
        feedback = feedback.ToUpper();

        var greenPositions = new Dictionary<int, char>();
        var yellowLetters = new Dictionary<char, int>();
        var redLetters = new HashSet<char>();

        for (int i = 0; i < guess.Length; i++)
        {
            char letter = guess[i];
            char fb = feedback[i];

            if (fb == 'G')
            {
                greenPositions[i] = letter;
                yellowLetters[letter] = yellowLetters.GetValueOrDefault(letter, 0) + 1;
            }
            else if (fb == 'Y')
            {
                yellowLetters[letter] = yellowLetters.GetValueOrDefault(letter, 0) + 1;
            }
            else if (fb == 'R')
            {
                redLetters.Add(letter);
            }
        }

        foreach (var kvp in greenPositions)
        {
            if (word[kvp.Key] != kvp.Value)
            {
                return false;
            }
        }

        var wordCounter = word.GroupBy(c => c).ToDictionary(g => g.Key, g => g.Count());
        foreach (var kvp in yellowLetters)
        {
            if (wordCounter.GetValueOrDefault(kvp.Key, 0) < kvp.Value)
            {
                return false;
            }
        }

        for (int i = 0; i < guess.Length; i++)
        {
            if (feedback[i] == 'Y' && word[i] == guess[i])
            {
                return false;
            }
        }

        foreach (char letter in redLetters)
        {
            int requiredCount = yellowLetters.GetValueOrDefault(letter, 0);
            if (wordCounter.GetValueOrDefault(letter, 0) > requiredCount)
            {
                return false;
            }
        }

        return true;
    }

    private static List<string> FilterWords(List<string> guesses, List<string> feedbacks, string[] wordList)
    {
        var possibleWords = wordList.ToList();

        for (int i = 0; i < guesses.Count; i++)
        {
            possibleWords = possibleWords.Where(word => IsValidWord(word, guesses[i], feedbacks[i])).ToList();
        }

        return possibleWords;
    }

    private static List<string> SuggestNextGuess(List<string> possibleWords)
    {
        if (possibleWords.Count <= 5)
        {
            return possibleWords;
        }

        var letterFreq = new Dictionary<char, int>();
        foreach (string word in possibleWords)
        {
            foreach (char letter in word.Distinct())
            {
                letterFreq[letter] = letterFreq.GetValueOrDefault(letter, 0) + 1;
            }
        }

        var wordScores = possibleWords.Select(word => new
        {
            Score = word.Distinct().Sum(letter => letterFreq[letter]),
            Word = word
        }).OrderByDescending(x => x.Score).Take(5).Select(x => x.Word).ToList();

        return wordScores;
    }

    static void Main()
    {
        Console.WriteLine("=" + new string('=', 59));
        Console.WriteLine("Enhanced Wordle Combinations Finder");
        Console.WriteLine("=" + new string('=', 59));
        Console.WriteLine("\nInstructions:");
        Console.WriteLine("  - Enter your guess (5-letter word)");
        Console.WriteLine("  - Enter feedback: G (green), Y (yellow), R (red)");
        Console.WriteLine("  - Type 'done' when finished entering guesses");
        Console.WriteLine("  - Type 'quit' to exit\n");
        Console.WriteLine("Example:");
        Console.WriteLine("  Guess: crane");
        Console.WriteLine("  Feedback: GYRRR (C is green, R is yellow, rest are red)\n");

        var guesses = new List<string>();
        var feedbacks = new List<string>();

        while (true)
        {
            Console.Write("Enter guess (or 'done'/'quit'): ");
            string guessInput = Console.ReadLine()?.ToLower().Trim() ?? "";

            if (guessInput == "quit" || guessInput == "exit" || guessInput == "q")
            {
                Console.WriteLine("Goodbye!");
                break;
            }

            if (guessInput == "done")
            {
                break;
            }

            Console.Write("Enter feedback (G/Y/R): ");
            string feedbackInput = Console.ReadLine()?.ToUpper().Trim() ?? "";

            var (valid, error) = ValidateGuess(guessInput, feedbackInput);
            if (!valid)
            {
                Console.WriteLine($"❌ Error: {error}\n");
                continue;
            }

            guesses.Add(guessInput);
            feedbacks.Add(feedbackInput);

            var possibleWords = FilterWords(guesses, feedbacks, WORD_LIST);
            Console.WriteLine($"✓ Added guess. Remaining possibilities: {possibleWords.Count}\n");
        }

        if (!guesses.Any())
        {
            Console.WriteLine($"\n📊 No guesses provided. Total words in dictionary: {WORD_LIST.Length}");
            return;
        }

        var finalPossibleWords = FilterWords(guesses, feedbacks, WORD_LIST);

        Console.WriteLine("\n" + new string('=', 60));
        Console.WriteLine("RESULTS");
        Console.WriteLine(new string('=', 60));

        if (finalPossibleWords.Any())
        {
            Console.WriteLine($"\n✓ Found {finalPossibleWords.Count} possible word(s):\n");

            var sortedWords = finalPossibleWords.OrderBy(w => w).ToList();
            for (int i = 0; i < sortedWords.Count; i++)
            {
                Console.WriteLine($"  {i + 1,2}. {sortedWords[i].ToUpper()}");
            }

            if (finalPossibleWords.Count > 5)
            {
                Console.WriteLine("\n💡 Suggested next guesses (best letter coverage):");
                var suggestions = SuggestNextGuess(finalPossibleWords);
                foreach (string word in suggestions)
                {
                    Console.WriteLine($"  → {word.ToUpper()}");
                }
            }
        }
        else
        {
            Console.WriteLine("\n❌ No words match the given constraints.");
            Console.WriteLine("   Check your feedback entries for errors.");
        }

        Console.WriteLine("\n" + new string('=', 60));
    }
}
