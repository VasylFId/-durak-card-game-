// app/static/js/game.js
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded - starting game initialization");
    
    // Initialize Socket.IO connection
    const socket = io();
    
    // Game elements
    const loadingOverlay = document.getElementById('loadingOverlay');
    const loadingMessage = document.getElementById('loadingMessage');
    const gameContainer = document.querySelector('.game-container');
    const playerHand = document.getElementById('playerHand');
    const opponentHand = document.getElementById('opponentHand');
    const battleArea = document.getElementById('boardArea');
    const deckCount = document.getElementById('deckCounter');
    const trumpCard = document.getElementById('trumpCard');
    const trumpIndicator = document.getElementById('trumpIndicator');
    const gameStatus = document.getElementById('gameStatus');
    const btnTakeCards = document.getElementById('btnTakeCards');
    const btnSkipTurn = document.getElementById('btnSkipTurn');
    const btnEndGame = document.getElementById('btnEndGame');
    const playerInfo = document.getElementById('playerInfo');
    const opponentInfo = document.getElementById('opponentInfo');
    
    // Get game ID from URL or session storage
    const urlParams = new URLSearchParams(window.location.search);
    const gameId = urlParams.get('game_id') || sessionStorage.getItem('game_id');
    console.log("Game ID from URL or session:", gameId);
    
    // Game state
    let gameState = {
        gameId: gameId,
        hand: [],
        attackerName: '',
        defenderName: '',
        isPlayerTurn: false,
        board: [],
        deckSize: 0,
        opponentHandSize: 0,
        trumpCard: null,
        trumpSuit: null,
        selectedCardIndex: null,
        isGameOver: false,
        winner: null,
        processing: false
    };
    
    // Animation state
    let animationSequenceComplete = false;
    let gameStateReceived = false;
    
    // Socket event handlers
    socket.on('connect', function() {
        console.log('Connected to server');
        updateStatus('Connected to server');
    });
    
    socket.on('connection_response', function(data) {
        console.log('Connection response:', data);
        if (data.status === 'error') {
            showMessage(data.message, true);
        }
    });
    
    socket.on('game_state', function(state) {
        console.log('Game state received:', state);
        if (state.error) {
            showMessage(state.error, true);
            hideLoadingOverlay();
            return;
        }
        
        updateGameState(state);
        gameStateReceived = true;
        
        if (!animationSequenceComplete) {
            startLoadingAnimation();
        } else {
            renderGame();
        }
    });
    
    socket.on('game_updated', function(state) {
        console.log('Game state updated:', state);
        if (state.error) {
            showMessage(state.error, true);
            return;
        }
        
        updateGameState(state);
        renderGame();
    });
    
    socket.on('player_joined', function(data) {
        console.log(`Player ${data.username} joined the game`);
        updateStatus(`${data.username} joined the game`);
    });
    
    socket.on('error', function(data) {
        console.error('Socket error:', data.message);
        showMessage(data.message, true);
    });
    
    socket.on('game_over', function(data) {
        console.log('Game over:', data);
        let message = '';
        
        if (data.winner === 'draw') {
            message = "Game over! It's a draw!";
        } else if (data.winner && data.winner.includes('Player_')) {
            message = "Congratulations! You won the game!";
        } else {
            message = "Game over! You lost the game.";
        }
        
        gameState.isGameOver = true;
        gameState.winner = data.winner;
        
        showMessage(message, false, 5000);
        updateStatus(message);
        
        // Disable game controls
        if (btnTakeCards) btnTakeCards.style.display = 'none';
        if (btnSkipTurn) btnSkipTurn.style.display = 'none';
        
        // Change end game button text
        if (btnEndGame) btnEndGame.textContent = 'Return to Lobby';
        
        renderGame();
        
        // Dispatch game over event for modal
        window.dispatchEvent(new CustomEvent('gameOver', { 
            detail: { message: message }
        }));
    });
    
    // Game functions
    function updateGameState(state) {
        console.log("Updating game state with:", state);
        
        // Handle the trump card format from server
        if (state.trump_card) {
            state.trumpCard = state.trump_card;
            console.log("Received trump card:", state.trumpCard);
        }
        
        // Update game state with received data
        Object.assign(gameState, state);
        
        // Make sure to extract and set the trump suit
        if (gameState.trumpCard) {
            extractAndSetTrumpSuit(gameState.trumpCard);
        }
        
        updateStatusMessage();
    }
    
    function updateStatusMessage() {
        if (gameState.isGameOver) {
            if (gameState.winner === 'draw') {
                updateStatus("Game over! It's a draw!");
            } else if (gameState.winner && gameState.winner.includes('Player_')) {
                updateStatus("Congratulations! You won the game!");
            } else {
                updateStatus("Game over! You lost the game.");
            }
            return;
        }
        
        // Get player's name
        const playerName = playerInfo ? playerInfo.textContent.split(' ')[0] : 'You';
        
        if (gameState.isPlayerTurn) {
            // It's player's turn - show appropriate message and buttons
            if (gameState.attackerName === playerName || gameState.attackerName.includes('Player_')) {
                updateStatus("It's your turn to attack");
                if (btnSkipTurn) btnSkipTurn.style.display = 'block';
                if (btnTakeCards) btnTakeCards.style.display = 'none';
            } else {
                updateStatus("It's your turn to defend");
                if (btnSkipTurn) btnSkipTurn.style.display = 'none';
                if (btnTakeCards) btnTakeCards.style.display = 'block';
            }
        } else {
            // It's opponent's turn
            if (gameState.attackerName === playerName || gameState.attackerName.includes('Player_')) {
                updateStatus("Opponent is defending...");
            } else {
                updateStatus("Opponent is attacking...");
            }
            
            if (btnSkipTurn) btnSkipTurn.style.display = 'none';
            if (btnTakeCards) btnTakeCards.style.display = 'none';
        }
    }
    
    function startLoadingAnimation() {
        // Show loading overlay and messages
        showLoadingOverlay();
        updateLoadingMessage('Shuffling cards...');
        
        setTimeout(() => updateLoadingMessage('Dealing cards...'), 500);
        setTimeout(() => updateLoadingMessage('Setting up the game...'), 1000);
        
        // Complete loading after delay
        setTimeout(() => {
            hideLoadingOverlay();
            animationSequenceComplete = true;
            renderGame();
        }, 1500);
    }
    
    function showLoadingOverlay() {
        if (loadingOverlay) {
            loadingOverlay.style.display = 'flex';
        }
        
        if (gameContainer) {
            gameContainer.style.opacity = '0.3';
        }
    }
    
    function hideLoadingOverlay() {
        if (loadingOverlay) {
            loadingOverlay.style.opacity = '0';
            setTimeout(() => {
                loadingOverlay.style.display = 'none';
            }, 300);
        }
        
        if (gameContainer) {
            gameContainer.style.opacity = '1';
        }
    }
    
    function updateLoadingMessage(message) {
        if (loadingMessage) {
            loadingMessage.textContent = message;
        }
    }
    
    function renderGame() {
        console.log("Rendering game state:", gameState);
        
        // Render player's hand
        renderPlayerHand();
        
        // Render opponent's hand
        renderOpponentHand();
        
        // Render battle area
        renderBattleArea();
        
        // Update deck count
        if (deckCount) {
            deckCount.textContent = gameState.deckSize;
        }
        
        // Update trump card and indicator
        renderTrumpCard();
        
        // Update player info
        updatePlayerInfo();
    }
    
    function renderPlayerHand() {
        if (!playerHand) return;
        
        // Store the current selection
        const selectedIndex = gameState.selectedCardIndex;
        
        playerHand.innerHTML = '';
        
        // Calculate the maximum width for the hand
        const handWidth = playerHand.offsetWidth;
        const cardWidth = 100; // Width of each card in pixels
        const cardCount = gameState.hand.length;
        
        // Determine overlap between cards
        let overlap = 0;
        if (cardCount > 1) {
            const maxCardsWithoutOverlap = Math.floor(handWidth / cardWidth);
            if (cardCount > maxCardsWithoutOverlap) {
                overlap = Math.min(cardWidth * 0.7, ((cardCount * cardWidth) - handWidth) / (cardCount - 1));
            }
        }
        
        // Calculate the total width of all cards with overlap
        const totalWidth = cardCount > 0 ? (cardWidth * cardCount) - ((cardCount - 1) * overlap) : 0;
        // Calculate starting position to center the hand
        const startX = (handWidth - totalWidth) / 2;
        
        gameState.hand.forEach((cardStr, index) => {
            const cardEl = document.createElement('div');
            cardEl.className = 'card';
            
            if (index === selectedIndex) {
                cardEl.classList.add('selected');
            }
            
            // Position card with fixed left spacing, centered in the hand
            const leftPosition = startX + index * (cardWidth - overlap);
            cardEl.style.position = 'absolute';
            cardEl.style.left = `${leftPosition}px`;
            cardEl.style.zIndex = index + 1; // Ensure proper stacking
            
            // Disable card if it's not player's turn or game is over
            if (!gameState.isPlayerTurn || gameState.isGameOver) {
                cardEl.style.pointerEvents = 'none';
                cardEl.style.opacity = '0.7';
            }
            
            cardEl.dataset.cardIndex = index;
            cardEl.innerHTML = renderCardInnerHTML(cardStr);
            
            // Add animation class for newly dealt cards
            if (animationSequenceComplete) {
                cardEl.classList.add('deal-animation');
                cardEl.style.animationDelay = `${index * 0.1}s`;
            }
            
            // Add event listeners for card selection
            cardEl.addEventListener('click', function() {
                selectCard(index);
            });
            
            // Add double-click event to play the card
            cardEl.addEventListener('dblclick', function() {
                if (gameState.selectedCardIndex === index) {
                    playCard(index);
                }
            });
            
            playerHand.appendChild(cardEl);
        });
    }
    
    function renderOpponentHand() {
        if (!opponentHand) return;
        
        opponentHand.innerHTML = '';
        
        // Calculate the maximum width for the hand
        const handWidth = opponentHand.offsetWidth;
        const cardWidth = 100; // Width of each card in pixels
        const cardCount = gameState.opponentHandSize;
        
        // Determine overlap between cards
        let overlap = 0;
        if (cardCount > 1) {
            const maxCardsWithoutOverlap = Math.floor(handWidth / cardWidth);
            if (cardCount > maxCardsWithoutOverlap) {
                overlap = Math.min(cardWidth * 0.7, ((cardCount * cardWidth) - handWidth) / (cardCount - 1));
            }
        }
        
        // Calculate the total width of all cards with overlap
        const totalWidth = cardCount > 0 ? (cardWidth * cardCount) - ((cardCount - 1) * overlap) : 0;
        // Calculate starting position to center the hand
        const startX = (handWidth - totalWidth) / 2;
        
        for (let i = 0; i < gameState.opponentHandSize; i++) {
            const cardBack = document.createElement('div');
            cardBack.className = 'card-back';
            
            // Position card with fixed left spacing, centered in the hand
            const leftPosition = startX + i * (cardWidth - overlap);
            cardBack.style.position = 'absolute';
            cardBack.style.left = `${leftPosition}px`;
            cardBack.style.zIndex = i + 1; // Ensure proper stacking
            
            // Add animation class for newly dealt cards
            if (animationSequenceComplete) {
                cardBack.classList.add('deal-animation');
                cardBack.style.animationDelay = `${i * 0.1}s`;
            }
            
            opponentHand.appendChild(cardBack);
        }
    }
    
    function renderBattleArea() {
        if (!battleArea) return;
        
        battleArea.innerHTML = '';
        
        // Group cards into attack-defense pairs
        const pairs = [];
        let attackCard = null;
        
        gameState.board.forEach(cardStr => {
            if (!attackCard) {
                attackCard = cardStr;
            } else {
                pairs.push({
                    attack: attackCard,
                    defense: cardStr
                });
                attackCard = null;
            }
        });
        
        // If there's an unpaired attack card
        if (attackCard) {
            pairs.push({
                attack: attackCard,
                defense: null
            });
        }
        
        // Render card pairs
        pairs.forEach((pair, index) => {
            const pairContainer = document.createElement('div');
            pairContainer.className = 'attack-pair';
            
            // Create attack card
            const attackDiv = document.createElement('div');
            attackDiv.className = 'card attack-card';
            attackDiv.innerHTML = renderCardInnerHTML(pair.attack);
            
            // Add play animation for newly added cards
            if (animationSequenceComplete) {
                attackDiv.classList.add('play-animation');
            }
            
            pairContainer.appendChild(attackDiv);
            
            // Create defense card if present
            if (pair.defense) {
                const defenseDiv = document.createElement('div');
                defenseDiv.className = 'card defense-card';
                defenseDiv.innerHTML = renderCardInnerHTML(pair.defense);
                
                // Add play animation for newly added cards
                if (animationSequenceComplete) {
                    defenseDiv.classList.add('play-animation');
                }
                
                pairContainer.appendChild(defenseDiv);
            }
            
            battleArea.appendChild(pairContainer);
        });
        
        // Show a message if board is empty
        if (pairs.length === 0) {
            const emptyMessage = document.createElement('div');
            emptyMessage.className = 'empty-board-indicator';
            emptyMessage.textContent = 'Board is empty. Play a card to start.';
            battleArea.appendChild(emptyMessage);
        }
    }
    
    function renderTrumpCard() {
        if (!trumpCard || !trumpIndicator) return;
        
        // Debug the trump card data
        console.log("Rendering trump card:", gameState.trumpCard);
        console.log("Trump suit:", gameState.trumpSuit);
        
        // Render trump card if available
        if (gameState.trumpCard) {
            // Make sure the trump card has the 'card' class
            trumpCard.classList.add('card');
            trumpCard.classList.add('trump-card');
            
            // Format the card string for rendering
            let formattedCardStr = gameState.trumpCard;
            console.log("Trump card string before formatting:", formattedCardStr);
            
            // Use our card rendering function
            trumpCard.innerHTML = renderCardInnerHTML(formattedCardStr);
            
            // Extract and set the trump suit
            extractAndSetTrumpSuit(formattedCardStr);
            
            // Update the trump indicator text
            if (gameState.trumpSuit) {
                // Determine suit name for display
                let suitName = getSuitName(gameState.trumpSuit);
                trumpIndicator.textContent = `Trump: ${gameState.trumpSuit} (${suitName})`;
            } else {
                trumpIndicator.textContent = 'Trump: ' + formattedCardStr;
            }
        } else {
            // No trump card
            trumpCard.innerHTML = '';
            trumpCard.classList.remove('card');
            trumpIndicator.textContent = 'Trump: None';
        }
    }

    function extractAndSetTrumpSuit(cardStr) {
        if (!cardStr) return;
        
        // Try various methods to extract the suit
        
        // Method 1: Simple character check
        if (cardStr.includes('♥')) {
            gameState.trumpSuit = '♥';
        } else if (cardStr.includes('♦')) {
            gameState.trumpSuit = '♦';
        } else if (cardStr.includes('♣')) {
            gameState.trumpSuit = '♣';
        } else if (cardStr.includes('♠')) {
            gameState.trumpSuit = '♠';
        } 
        // Method 2: Regex pattern matching
        else {
            const suitMatch = cardStr.match(/([♥♦♣♠])/);
            if (suitMatch) {
                gameState.trumpSuit = suitMatch[1];
            }
        }
        
        console.log("Extracted trump suit:", gameState.trumpSuit);
    }

    function getSuitName(suitChar) {
        if (!suitChar) return 'Unknown';
        
        if (suitChar.includes('♥')) return 'Hearts';
        if (suitChar.includes('♦')) return 'Diamonds';
        if (suitChar.includes('♣')) return 'Clubs';
        if (suitChar.includes('♠')) return 'Spades';
        
        return 'Unknown';
    }
    
    function updatePlayerInfo() {
        // Update player info
        if (playerInfo) {
            const playerName = playerInfo.textContent.split(' ')[0];
            playerInfo.innerHTML = `<i class="fas fa-user me-2"></i>${playerName} (${gameState.hand.length} cards)`;
        }
        
        // Update opponent info - Change from 'Opponent' to 'AI Opponent' in AI mode
        if (opponentInfo) {
            const opponentName = gameState.defenderName && gameState.defenderName.includes('AI') ? 
                'AI Opponent' : 
                (gameState.attackerName && gameState.attackerName.includes('AI') ? 
                    'AI Opponent' : 'Opponent');
                    
            opponentInfo.innerHTML = `<i class="fas fa-user-alt me-2"></i>${opponentName} (${gameState.opponentHandSize} cards)`;
        }
    }
    
function renderCardInnerHTML(cardStr) {
    if (!cardStr) return '';

    console.log("Processing card string:", cardStr);
    
    // Extract both rank and suit, accounting for different formats and emoji variations
    let suitChar, rank;
    
    // Unicode variations of suit characters including emoji variants
    const heartsPattern = /[♥♡❤]/;
    const diamondsPattern = /[♦♢◆]/;
    const clubsPattern = /[♣♧]/;
    const spadesPattern = /[♠♤]/;
    
    // Try different card string formats
    let match;
    
    // Format 1: Suit first, then rank (e.g., "♠️8")
    match = cardStr.match(/([♥♦♣♠♡♢♧♤])(?:️)?([A-Z0-9]+)/i);
    if (match) {
        [_, suitChar, rank] = match;
    } 
    // Format 2: Rank first, then suit (e.g., "8♠️")
    else {
        match = cardStr.match(/([A-Z0-9]+)([♥♦♣♠♡♢♧♤])(?:️)?/i);
        if (match) {
            [_, rank, suitChar] = match;
        } 
        // Format 3: Last resort - try to identify any suit and any digit/letter
        else {
            // Find any suit character
            if (heartsPattern.test(cardStr)) {
                suitChar = '♥';
            } else if (diamondsPattern.test(cardStr)) {
                suitChar = '♦';
            } else if (clubsPattern.test(cardStr)) {
                suitChar = '♣';
            } else if (spadesPattern.test(cardStr)) {
                suitChar = '♠';
            } else {
                suitChar = '?';
            }
            
            // Find any rank character
            const rankMatch = cardStr.match(/([A-Z0-9]+)/i);
            rank = rankMatch ? rankMatch[1] : '?';
            
            console.warn("Using fallback parsing for card:", cardStr);
        }
    }
    
    if (!suitChar || !rank) {
        console.error("Failed to parse card string:", cardStr);
        return `<div class="card-inner">
                  <div class="card-top">Error</div>
                  <div class="card-center">?</div>
                  <div class="card-bottom">Error</div>
                </div>`;
    }
    
    console.log("Parsed suit:", suitChar, "rank:", rank);
    
    // Determine suit class and HTML entity
    let suitClass, suitHTML;
    
    // Handle different suit characters
    if (heartsPattern.test(suitChar)) {
        suitClass = 'hearts';
        suitHTML = '&hearts;';
    } else if (diamondsPattern.test(suitChar)) {
        suitClass = 'diamonds';
        suitHTML = '&diams;';
    } else if (clubsPattern.test(suitChar)) {
        suitClass = 'clubs';
        suitHTML = '&clubs;';
    } else {
        // Default to spades or unknown
        suitClass = 'spades';
        suitHTML = '&spades;';
    }
    
    // Check if this is a trump suit - use a more flexible comparison for emoji variants
    let isTrump = '';
    if (gameState.trumpSuit) {
        if (
            (heartsPattern.test(suitChar) && heartsPattern.test(gameState.trumpSuit)) ||
            (diamondsPattern.test(suitChar) && diamondsPattern.test(gameState.trumpSuit)) ||
            (clubsPattern.test(suitChar) && clubsPattern.test(gameState.trumpSuit)) ||
            (spadesPattern.test(suitChar) && spadesPattern.test(gameState.trumpSuit))
        ) {
            isTrump = 'trump-suit';
        }
    }

    return `
        <div class="card-inner">
            <div class="card-top">
                <span class="card-rank">${rank}</span>
                <span class="card-suit ${suitClass} ${isTrump}">${suitHTML}</span>
            </div>
            <div class="card-center">
                <span class="card-suit ${suitClass} ${isTrump}">${suitHTML}</span>
            </div>
            <div class="card-bottom">
                <span class="card-rank">${rank}</span>
                <span class="card-suit ${suitClass} ${isTrump}">${suitHTML}</span>
            </div>
        </div>
    `;
    }
    function updateStatus(message) {
        if (gameStatus) {
            gameStatus.innerHTML = `<i class="fas fa-info-circle me-2"></i>${message}`;
        }
    }

    function updateCardSelection() {
        // Get all card elements in player hand
        const cardElements = playerHand.querySelectorAll('.card');
        
        // Update each card's selected state based on gameState.selectedCardIndex
        cardElements.forEach((card, index) => {
            if (index === gameState.selectedCardIndex) {
                card.classList.add('selected');
            } else {
                card.classList.remove('selected');
            }
        });
    }
    
    function selectCard(index) {
        // Check if it's player's turn
        if (!gameState.isPlayerTurn) {
            showMessage("It's not your turn");
            return;
        }
        
        // Check if game is over
        if (gameState.isGameOver) {
            showMessage("The game is already over");
            return;
        }
        
        // Check if we're already processing a move
        if (gameState.processing) {
            return;
        }
        
        // Set the selected card index
        gameState.selectedCardIndex = index;
        
        // Just update the visual state without re-rendering everything
        updateCardSelection();
        
        // Play the card
        playCard(index);
    }

    function playCard(index) {
        // Send the play card event to the server
        socket.emit('play_card', {
            game_id: gameState.gameId,
            card_index: index
        });
        
        // Reset the processing flag after a short delay
        setTimeout(() => {
            gameState.processing = false;
        }, 500);
    }
    
    function takeTurnCards() {
        // Check if we're already processing a move
        if (gameState.processing) {
            return;
        }
        
        gameState.processing = true;
        
        // Send the take cards event to the server
        socket.emit('take_cards', {
            game_id: gameState.gameId
        });
        
        // Reset the processing flag after a short delay
        setTimeout(() => {
            gameState.processing = false;
        }, 500);
    }
    
    function passTurn() {
        // Check if we're already processing a move
        if (gameState.processing) {
            return;
        }
        
        gameState.processing = true;
        
        // Send the skip turn event to the server
        socket.emit('skip_turn', {
            game_id: gameState.gameId
        });
        
        // Reset the processing flag after a short delay
        setTimeout(() => {
            gameState.processing = false;
        }, 500);
    }
    
    function showMessage(message, isError = false, duration = 3000) {
        console.log("Showing message:", message, "isError:", isError);
        
        const existingMessages = document.querySelectorAll('.game-message');
        existingMessages.forEach(msg => msg.remove());
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'game-message';
        if (isError) {
            messageDiv.classList.add('error-message');
        }
        messageDiv.textContent = message;
        
        document.body.appendChild(messageDiv);
        
        setTimeout(() => {
            messageDiv.style.opacity = '0';
            setTimeout(() => {
                messageDiv.remove();
            }, 300);
        }, duration);
    }
    
    function joinGame(gameId) {
        gameState.gameId = gameId;
        
        // Show loading overlay
        showLoadingOverlay();
        
        // Join the game room
        socket.emit('join_game', {
            game_id: gameId
        });
        
        // Store game ID in session storage
        sessionStorage.setItem('game_id', gameId);
        
        updateStatus('Joining game...');
    }
    
    // Event listeners for game controls
    if (btnTakeCards) {
        btnTakeCards.addEventListener('click', function() {
            if (gameState.isGameOver) {
                showMessage("The game is already over");
                return;
            }
            takeTurnCards();
        });
    }
    
    if (btnSkipTurn) {
        btnSkipTurn.addEventListener('click', function() {
            if (gameState.isGameOver) {
                showMessage("The game is already over");
                return;
            }
            passTurn();
        });
    }
    
    if (btnEndGame) {
        btnEndGame.addEventListener('click', function() {
            if (gameState.isGameOver) {
                window.location.href = '/game';
                return;
            }
            
            if (confirm('Are you sure you want to leave the game?')) {
                window.location.href = '/game';
            }
        });
    }
    
    // Start the game if we have a game ID
    if (gameId) {
        console.log("Game ID found, joining game:", gameId);
        joinGame(gameId);
        
        // Failsafe - if game state isn't received within 5 seconds, hide loading
        setTimeout(() => {
            if (!gameStateReceived) {
                hideLoadingOverlay();
                showMessage('Game is taking longer than expected to load.', true);
            }
        }, 5000);
    } else {
        console.log("No game ID found");
        hideLoadingOverlay();
    }
    
    // Function to start a new game (for public API)
    function startNewGame(againstAI = true) {
        // Reset state
        gameState = {
            gameId: null,
            hand: [],
            attackerName: '',
            defenderName: '',
            isPlayerTurn: false,
            board: [],
            deckSize: 0,
            opponentHandSize: 0,
            trumpCard: null,
            trumpSuit: null,
            selectedCardIndex: null,
            isGameOver: false,
            winner: null,
            processing: false
        };
        
        animationSequenceComplete = false;
        gameStateReceived = false;
        
        // Show loading overlay
        showLoadingOverlay();
        
        // Send the start game event
        socket.emit('start_game', {
            against_ai: againstAI
        });
        
        updateStatus('Starting new game...');
    }
    
    // Expose public API
    window.durakGame = {
        startNewGame,
        joinGame
    };
});