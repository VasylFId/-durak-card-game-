// app/static/js/game.js
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Socket.IO connection
    const socket = io();
    
    // Game elements
    const gameBoard = document.querySelector('.game-board');
    const playerHand = document.querySelector('.player-hand');
    const opponentHand = document.querySelector('.opponent-hand');
    const battleArea = document.querySelector('.battle-area');
    const deckCount = document.querySelector('.deck-count');
    const trumpCard = document.querySelector('.trump-card');
    const btnTake = document.querySelector('.btn-take');
    const btnPass = document.querySelector('.btn-pass');
    
    // Game state
    let gameState = {
        gameId: null,
        hand: [],
        attackerName: '',
        defenderName: '',
        isPlayerTurn: false,
        board: [],
        deckSize: 0,
        opponentHandSize: 0,
        trumpCard: null,
        selectedCard: null
    };
    
    // Get game ID from URL or session storage
    const urlParams = new URLSearchParams(window.location.search);
    const gameId = urlParams.get('game_id') || sessionStorage.getItem('game_id');
    
    if (gameId) {
        joinGame(gameId);
    }
    
    // Socket event handlers
    socket.on('connect', function() {
        console.log('Connected to server');
    });
    
    socket.on('game_state', function(state) {
        updateGameState(state);
        renderGame();
    });
    
    socket.on('game_updated', function(state) {
        updateGameState(state);
        renderGame();
    });
    
    socket.on('player_joined', function(data) {
        console.log(`Player ${data.username} joined the game`);
    });
    
    socket.on('error', function(data) {
        showMessage(data.message);
    });
    
    // Game functions
    function joinGame(gameId) {
        socket.emit('join_game', {
            game_id: gameId
        });
    }
    
    function updateGameState(state) {
        if (state.error) {
            showMessage(state.error);
            return;
        }
        
        gameState = {
            ...gameState,
            ...state
        };
    }
    
    function renderGame() {
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
        
        // Update trump card
        if (trumpCard && gameState.trumpCard) {
            trumpCard.innerHTML = renderCardContent(gameState.trumpCard);
        }
        
        // Update game controls
        updateGameControls();
    }
    
    function renderPlayerHand() {
        if (!playerHand) return;
        
        playerHand.innerHTML = '';
        
        gameState.hand.forEach((cardStr, index) => {
            const cardEl = document.createElement('div');
            cardEl.className = 'player-card';
            cardEl.dataset.cardIndex = index;
            cardEl.innerHTML = renderCardContent(cardStr);
            
            cardEl.addEventListener('click', function() {
                selectCard(index);
            });
            
            playerHand.appendChild(cardEl);
        });
    }
    
    function renderOpponentHand() {
        if (!opponentHand) return;
        
        opponentHand.innerHTML = '';
        
        for (let i = 0; i < gameState.opponentHandSize; i++) {
            const cardBack = document.createElement('div');
            cardBack.className = 'card-back';
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
        pairs.forEach(pair => {
            const pairDiv = document.createElement('div');
            pairDiv.className = 'card-pair';
            
            const attackDiv = document.createElement('div');
            attackDiv.className = 'attack-card';
            attackDiv.innerHTML = renderCardContent(pair.attack);
            pairDiv.appendChild(attackDiv);
            
            if (pair.defense) {
                const defenseDiv = document.createElement('div');
                defenseDiv.className = 'defense-card';
                defenseDiv.innerHTML = renderCardContent(pair.defense);
                pairDiv.appendChild(defenseDiv);
            }
            
            battleArea.appendChild(pairDiv);
        });
    }
    
    function renderCardContent(cardStr) {
        if (!cardStr) return '';
        
        const match = cardStr.match(/([♥️♦️♣️♠️])([6-9]|10|J|Q|K|A)/);
        if (!match) return cardStr;
        
        const [_, suit, rank] = match;
        let suitClass = '';
        
        switch (suit) {
            case '♥️':
                suitClass = 'suit-hearts';
                break;
            case '♦️':
                suitClass = 'suit-diamonds';
                break;
            case '♣️':
                suitClass = 'suit-clubs';
                break;
            case '♠️':
                suitClass = 'suit-spades';
                break;
        }
        
        return `
            <div class="card-rank">${rank}</div>
            <div class="card-suit ${suitClass} top-left">${suit}</div>
            <div class="card-suit ${suitClass} bottom-right">${suit}</div>
        `;
    }
    
    function updateGameControls() {
        if (!btnTake || !btnPass) return;
        
        const isDefender = gameState.defenderName === playerName;
        const isAttacker = gameState.attackerName === playerName;
        
        btnTake.style.display = isDefender && gameState.isPlayerTurn ? 'block' : 'none';
        btnPass.style.display = gameState.isPlayerTurn ? 'block' : 'none';
        
        btnTake.disabled = !gameState.isPlayerTurn;
        btnPass.disabled = !gameState.isPlayerTurn;
    }
    
    function selectCard(index) {
        if (!gameState.isPlayerTurn) {
            showMessage("It's not your turn");
            return;
        }
        
        const card = gameState.hand[index];
        
        // Toggle selection
        if (gameState.selectedCard === index) {
            gameState.selectedCard = null;
            renderPlayerHand();
        } else {
            gameState.selectedCard = index;
            renderPlayerHand();
            
            // Highlight selected card
            const cardElements = document.querySelectorAll('.player-card');
            cardElements[index].classList.add('selected');
            
            // Play card
            playCard(index);
        }
    }
    
    function playCard(index) {
        socket.emit('play_card', {
            game_id: gameState.gameId,
            card_index: index
        });
    }
    
    function takeTurnCards() {
        socket.emit('take_cards', {
            game_id: gameState.gameId
        });
    }
    
    function passTurn() {
        socket.emit('skip_turn', {
            game_id: gameState.gameId
        });
    }
    
    function showMessage(message, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'game-message';
        if (isError) {
            messageDiv.classList.add('error-message');
        }
        messageDiv.textContent = message;
        
        gameBoard.appendChild(messageDiv);
        
        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }
    
    // Event listeners for game controls
    if (btnTake) {
        btnTake.addEventListener('click', function() {
            takeTurnCards();
        });
    }
    
    if (btnPass) {
        btnPass.addEventListener('click', function() {
            passTurn();
        });
    }
    
    // Request initial game state
    if (gameId) {
        socket.emit('request_game_state', {
            game_id: gameId
        });
    }
    
    // Function to start a new game
    function startNewGame(againstAI = true) {
        socket.emit('start_game', {
            against_ai: againstAI
        });
    }
    
    // Expose public functions
    window.durakGame = {
        startNewGame,
        joinGame
    };
});