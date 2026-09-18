/**
 * Lightweight in-browser Wordle candidate filter.
 * Matches G/Y/R semantics used by Lexicon Locksmith CLI.
 * Does not fetch or display NYT answers.
 */
(function () {
  "use strict";

  const wordlistUrl = "wordlist.txt";
  let allWords = [];
  let guesses = [];

  const els = {
    status: document.getElementById("demo-status"),
    guessInput: document.getElementById("demo-guess"),
    feedbackInput: document.getElementById("demo-feedback"),
    addBtn: document.getElementById("demo-add"),
    undoBtn: document.getElementById("demo-undo"),
    resetBtn: document.getElementById("demo-reset"),
    guessList: document.getElementById("demo-guesses"),
    candidates: document.getElementById("demo-candidates"),
    count: document.getElementById("demo-count"),
  };

  if (!els.addBtn) return;

  function setStatus(msg) {
    if (els.status) els.status.textContent = msg;
  }

  function normalizeFeedback(raw) {
    return String(raw || "")
      .toUpperCase()
      .replace(/[^GYR]/g, "");
  }

  /**
   * Filter words given guess + G/Y/R feedback.
   * G = letter correct & in position
   * Y = letter in word, wrong position
   * R = letter not in word (or excess duplicate)
   */
  function matchesConstraints(word, guessList) {
    for (let i = 0; i < guessList.length; i++) {
      const { guess, feedback } = guessList[i];
      if (!wordMatches(word, guess, feedback)) return false;
    }
    return true;
  }

  function wordMatches(word, guess, feedback) {
    const w = word.split("");
    const g = guess.split("");
    const f = feedback.split("");
    const remaining = {};

    // Greens first
    for (let i = 0; i < 5; i++) {
      if (f[i] === "G") {
        if (w[i] !== g[i]) return false;
        w[i] = null;
      }
    }

    // Count remaining letters in word
    for (let i = 0; i < 5; i++) {
      if (w[i] !== null) {
        remaining[w[i]] = (remaining[w[i]] || 0) + 1;
      }
    }

    // Yellows: must exist elsewhere
    for (let i = 0; i < 5; i++) {
      if (f[i] === "Y") {
        if (word[i] === g[i]) return false; // yellow can't be same position
        if (!remaining[g[i]]) return false;
        remaining[g[i]]--;
      }
    }

    // Reds: letter must not remain (handles duplicates)
    for (let i = 0; i < 5; i++) {
      if (f[i] === "R") {
        if (remaining[g[i]]) return false;
      }
    }

    return true;
  }

  function filterCandidates() {
    if (!guesses.length) return allWords.slice();
    return allWords.filter(function (w) {
      return matchesConstraints(w, guesses);
    });
  }

  function renderGuesses() {
    els.guessList.innerHTML = "";
    guesses.forEach(function (item, idx) {
      const li = document.createElement("li");
      li.className = "guess-chip";
      li.setAttribute("aria-label", "Guess " + item.guess + " feedback " + item.feedback);

      for (let i = 0; i < 5; i++) {
        const tile = document.createElement("span");
        tile.className = "tile " + item.feedback[i];
        tile.textContent = item.guess[i].toUpperCase();
        tile.title = item.feedback[i];
        li.appendChild(tile);
      }

      const rm = document.createElement("button");
      rm.type = "button";
      rm.setAttribute("aria-label", "Remove guess " + (idx + 1));
      rm.textContent = "×";
      rm.addEventListener("click", function () {
        guesses.splice(idx, 1);
        update();
      });
      li.appendChild(rm);
      els.guessList.appendChild(li);
    });
  }

  function renderCandidates(list) {
    const maxShow = 200;
    els.count.textContent = String(list.length);
    els.candidates.innerHTML = "";

    if (!list.length) {
      const empty = document.createElement("span");
      empty.className = "empty";
      empty.textContent = guesses.length
        ? "No candidates match. Check feedback or undo a guess."
        : "Word list not loaded yet.";
      els.candidates.appendChild(empty);
      return;
    }

    const show = list.slice(0, maxShow);
    show.forEach(function (w) {
      const span = document.createElement("span");
      span.className = "word";
      span.textContent = w;
      els.candidates.appendChild(span);
    });

    if (list.length > maxShow) {
      const more = document.createElement("span");
      more.className = "empty";
      more.textContent = "… and " + (list.length - maxShow) + " more (use the CLI for full ranked lists)";
      els.candidates.appendChild(more);
    }
  }

  function update() {
    renderGuesses();
    renderCandidates(filterCandidates());
  }

  function addGuess() {
    const guess = String(els.guessInput.value || "")
      .toLowerCase()
      .replace(/[^a-z]/g, "");
    const feedback = normalizeFeedback(els.feedbackInput.value);

    if (guess.length !== 5) {
      setStatus("Enter a 5-letter guess.");
      els.guessInput.focus();
      return;
    }
    if (feedback.length !== 5) {
      setStatus("Feedback must be 5 characters using only G, Y, or R.");
      els.feedbackInput.focus();
      return;
    }

    guesses.push({ guess: guess, feedback: feedback });
    els.guessInput.value = "";
    els.feedbackInput.value = "";
    setStatus("Added guess. Candidates updated.");
    update();
    els.guessInput.focus();
  }

  els.addBtn.addEventListener("click", addGuess);
  els.undoBtn.addEventListener("click", function () {
    if (!guesses.length) {
      setStatus("Nothing to undo.");
      return;
    }
    guesses.pop();
    setStatus("Undid last guess.");
    update();
  });
  els.resetBtn.addEventListener("click", function () {
    guesses = [];
    setStatus("Cleared all guesses.");
    update();
  });

  [els.guessInput, els.feedbackInput].forEach(function (input) {
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        addGuess();
      }
    });
  });

  setStatus("Loading word list…");
  fetch(wordlistUrl)
    .then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status);
      return res.text();
    })
    .then(function (text) {
      allWords = text
        .split(/\r?\n/)
        .map(function (l) {
          return l.trim().toLowerCase();
        })
        .filter(function (w) {
          return /^[a-z]{5}$/.test(w);
        });
      // dedupe while preserving order
      const seen = Object.create(null);
      allWords = allWords.filter(function (w) {
        if (seen[w]) return false;
        seen[w] = true;
        return true;
      });
      setStatus("Loaded " + allWords.length + " words. Add guesses to filter.");
      update();
    })
    .catch(function () {
      setStatus("Could not load wordlist.txt. The CLI still works from the GitHub repo.");
      allWords = [];
      update();
    });
})();
