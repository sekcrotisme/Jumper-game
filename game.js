const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let player = { x: 50, y: 250, width: 30, height: 30, vy: 0, gravity: 0.8, jumpPower: -12, onGround: true };
let obstacles = [];
let score = 0;
let gameSpeed = 5;
let gameOver = false;

document.addEventListener("keydown", function(e) {
  if (e.code === "Space" && player.onGround) {
    player.vy = player.jumpPower;
    player.onGround = false;
  }
});

function spawnObstacle() {
  const height = 30 + Math.random() * 30;
  obstacles.push({ x: canvas.width, y: canvas.height - height, width: 20, height: height });
}

function update() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw player
  player.vy += player.gravity;
  player.y += player.vy;
  if (player.y >= canvas.height - player.height) {
    player.y = canvas.height - player.height;
    player.vy = 0;
    player.onGround = true;
  }
  ctx.fillStyle = "#00ffcc";
  ctx.fillRect(player.x, player.y, player.width, player.height);

  // Draw obstacles
  for (let i = 0; i < obstacles.length; i++) {
    obstacles[i].x -= gameSpeed;
    ctx.fillStyle = "#ff4444";
    ctx.fillRect(obstacles[i].x, obstacles[i].y, obstacles[i].width, obstacles[i].height);

    // Collision
    if (player.x < obstacles[i].x + obstacles[i].width &&
        player.x + player.width > obstacles[i].x &&
        player.y < obstacles[i].y + obstacles[i].height &&
        player.y + player.height > obstacles[i].y) {
      gameOver = true;
    }
  }

  obstacles = obstacles.filter(ob => ob.x + ob.width > 0);

  // Score & spawn
  score++;
  document.getElementById("score").textContent = "Skor: " + score;
  if (score % 100 === 0) spawnObstacle();

  if (!gameOver) requestAnimationFrame(update);
  else {
    ctx.fillStyle = "white";
    ctx.font = "24px Arial";
    ctx.fillText("Game Over! Refresh untuk bermain lagi", 200, 150);
  }
}

spawnObstacle();
update();
