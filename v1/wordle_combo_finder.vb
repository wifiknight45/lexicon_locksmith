Imports System
Imports System.Collections.Generic
Imports System.Linq

Module WordleFinder
    Private ReadOnly WORD_LIST As String() = {
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
    }

    Public Function ValidateGuess(guess As String, feedback As String) As (Boolean, String)
        If guess.Length <> 5 OrElse Not guess.All(AddressOf Char.IsLetter) Then
            Return (False, "Guess must be a 5-letter word containing only letters.")
        End If
        If feedback.Length <> 5 OrElse Not feedback.ToUpper().All(Function(c) "GYR".Contains(c)) Then
            Return (False, "Feedback must be 5 characters, each 'G' (green), 'Y' (yellow), or 'R' (red).")
        End If
        Return (True, "")
    End Function

    Public Function IsValidWord(word As String, guess As String, feedback As String) As Boolean
        Dim guessLower As String = guess.ToLower()
        Dim wordLower As String = word.ToLower()
        Dim feedbackUpper As String = feedback.ToUpper()

        Dim greenPositions As New Dictionary(Of Integer, Char)()
        Dim yellowLetters As New Dictionary(Of Char, Integer)()
        Dim redLetters As New HashSet(Of Char)()

        For i As Integer = 0 To guessLower.Length - 1
            Dim letter As Char = guessLower(i)
            Dim fb As Char = feedbackUpper(i)

            If fb = "G"c Then
                greenPositions(i) = letter
                If yellowLetters.ContainsKey(letter) Then
                    yellowLetters(letter) += 1
                Else
                    yellowLetters(letter) = 1
                End If
            ElseIf fb = "Y"c Then
                If yellowLetters.ContainsKey(letter) Then
                    yellowLetters(letter) += 1
                Else
                    yellowLetters(letter) = 1
                End If
            ElseIf fb = "R"c Then
                redLetters.Add(letter)
            End If
        Next

        For Each kvp In greenPositions
            If wordLower(kvp.Key) <> kvp.Value Then
                Return False
            End If
        Next

        Dim wordCounter As New Dictionary(Of Char, Integer)()
        For Each c In wordLower
            If wordCounter.ContainsKey(c) Then
                wordCounter(c) += 1
            Else
                wordCounter(c) = 1
            End If
        Next

        For Each kvp In yellowLetters
            Dim letter As Char = kvp.Key
            Dim minCount As Integer = kvp.Value
            If Not wordCounter.ContainsKey(letter) OrElse wordCounter(letter) < minCount Then
                Return False
            End If
        Next

        For i As Integer = 0 To guessLower.Length - 1
            Dim letter As Char = guessLower(i)
            Dim fb As Char = feedbackUpper(i)
            If fb = "Y"c AndAlso wordLower(i) = letter Then
                Return False
            End If
        Next

        For Each letter In redLetters
            Dim requiredCount As Integer = If(yellowLetters.ContainsKey(letter), yellowLetters(letter), 0)
            Dim actualCount As Integer = If(wordCounter.ContainsKey(letter), wordCounter(letter), 0)
            If actualCount > requiredCount Then
                Return False
            End If
        Next

        Return True
    End Function

    Public Function FilterWords(guesses As List(Of String), feedbacks As List(Of String), wordList As String()) As List(Of String)
        Dim possibleWords As New List(Of String)(wordList)

        For i As Integer = 0 To guesses.Count - 1
            possibleWords = possibleWords.Where(Function(word) IsValidWord(word, guesses(i), feedbacks(i))).ToList()
        Next

        Return possibleWords
    End Function

    Public Function SuggestNextGuess(possibleWords As List(Of String)) As List(Of String)
        If possibleWords.Count <= 5 Then
            Return possibleWords
        End If

        Dim letterFreq As New Dictionary(Of Char, Integer)()
        For Each word In possibleWords
            For Each letter In word.ToCharArray().Distinct()
                If letterFreq.ContainsKey(letter) Then
                    letterFreq(letter) += 1
                Else
                    letterFreq(letter) = 1
                End If
            Next
        Next

        Dim wordScores As New List(Of (Integer, String))()
        For Each word In possibleWords
            Dim score As Integer = word.ToCharArray().Distinct().Sum(Function(letter) If(letterFreq.ContainsKey(letter), letterFreq(letter), 0))
            wordScores.Add((score, word))
        Next

        wordScores.Sort(Function(x, y) y.Item1.CompareTo(x.Item1))
        Return wordScores.Take(5).Select(Function(x) x.Item2).ToList()
    End Function

    Sub Main()
        Console.WriteLine(New String("="c, 60))
        Console.WriteLine("Enhanced Wordle Combinations Finder")
        Console.WriteLine(New String("="c, 60))
        Console.WriteLine()
        Console.WriteLine("Instructions:")
        Console.WriteLine("  - Enter your guess (5-letter word)")
        Console.WriteLine("  - Enter feedback: G (green), Y (yellow), R (red)")
        Console.WriteLine("  - Type 'done' when finished entering guesses")
        Console.WriteLine("  - Type 'quit' to exit")
        Console.WriteLine()
        Console.WriteLine("Example:")
        Console.WriteLine("  Guess: crane")
        Console.WriteLine("  Feedback: GYRRR (C is green, R is yellow, rest are red)")
        Console.WriteLine()

        Dim guesses As New List(Of String)()
        Dim feedbacks As New List(Of String)()

        Do
            Dim guessInput As String
            Try
                Console.Write("Enter guess (or 'done'/'quit'): ")
                guessInput = Console.ReadLine().ToLower().Trim()
            Catch ex As Exception
                Console.WriteLine(vbCrLf & vbCrLf & "Exiting...")
                Exit Do
            End Try

            If guessInput = "quit" OrElse guessInput = "exit" OrElse guessInput = "q" Then
                Console.WriteLine("Goodbye!")
                Exit Do
            End If

            If guessInput = "done" Then
                Exit Do
            End If

            Dim feedbackInput As String
            Try
                Console.Write("Enter feedback (G/Y/R): ")
                feedbackInput = Console.ReadLine().ToUpper().Trim()
            Catch ex As Exception
                Console.WriteLine(vbCrLf & vbCrLf & "Exiting...")
                Exit Do
            End Try

            Dim result = ValidateGuess(guessInput, feedbackInput)
            If Not result.Item1 Then
                Console.WriteLine($"❌ Error: {result.Item2}" & vbCrLf)
                Continue Do
            End If

            guesses.Add(guessInput)
            feedbacks.Add(feedbackInput)

            Dim possibleWords = FilterWords(guesses, feedbacks, WORD_LIST)
            Console.WriteLine($"✓ Added guess. Remaining possibilities: {possibleWords.Count}" & vbCrLf)
        Loop

        If guesses.Count = 0 Then
            Console.WriteLine($"{vbCrLf}📊 No guesses provided. Total words in dictionary: {WORD_LIST.Length}")
            Return
        End If

        Dim finalPossibleWords = FilterWords(guesses, feedbacks, WORD_LIST)

        Console.WriteLine(vbCrLf & New String("="c, 60))
        Console.WriteLine("RESULTS")
        Console.WriteLine(New String("="c, 60))

        If finalPossibleWords.Count > 0 Then
            Console.WriteLine($"{vbCrLf}✓ Found {finalPossibleWords.Count} possible word(s):{vbCrLf}")

            Dim sortedWords = finalPossibleWords.OrderBy(Function(w) w).ToList()
            For i As Integer = 0 To sortedWords.Count - 1
                Console.WriteLine($"  {(i + 1).ToString().PadLeft(2)}. {sortedWords(i).ToUpper()}")
            Next

            If finalPossibleWords.Count > 5 Then
                Console.WriteLine($"{vbCrLf}💡 Suggested next guesses (best letter coverage):")
                Dim suggestions = SuggestNextGuess(finalPossibleWords)
                For Each word In suggestions
                    Console.WriteLine($"  → {word.ToUpper()}")
                Next
            End If
        Else
            Console.WriteLine($"{vbCrLf}❌ No words match the given constraints.")
            Console.WriteLine("   Check your feedback entries for errors.")
        End If

        Console.WriteLine(vbCrLf & New String("="c, 60))
    End Sub
End Module
