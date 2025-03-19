// Basic debug script to check if elements exist and are functioning
document.addEventListener('DOMContentLoaded', function() {
    console.log('Debug script loaded');
    
    // Check if key game elements exist
    const elementsToCheck = [
        'loadingOverlay',
        'gameStatus',
        'opponentHand',
        'opponentInfo',
        'deck',
        'deckCounter',
        'trumpCard',
        'trumpIndicator',
        'boardArea',
        'playerHand',
        'playerInfo',
        'btnTakeCards',
        'btnSkipTurn',
        'btnEndGame'
    ];
    
    elementsToCheck.forEach(id => {
        const element = document.getElementById(id);
        console.log(`Element '${id}' exists: ${!!element}`);
    });
    
    // Get game ID
    const urlParams = new URLSearchParams(window.location.search);
    const gameId = urlParams.get('game_id') || sessionStorage.getItem('game_id');
    console.log('Game ID:', gameId);
    
    // Add a forced display
    setTimeout(() => {
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
        }
        
        const gameContainer = document.querySelector('.game-container');
        if (gameContainer) {
            gameContainer.style.display = 'block';
            gameContainer.style.backgroundColor = '#1a5c2f';
            gameContainer.innerHTML += '<div class="alert alert-info mt-3">Debug message: Game container is visible now</div>';
        }
    }, 3000);
});