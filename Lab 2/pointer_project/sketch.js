// ===============================
// PiTFT Pointer Interaction
// Canvas: 240 x 135
// ===============================

let activeRegion = 1;

// Each region has its own pointer length
let pointerLengths = [0, 0, 0, 0];

// Whether each pointer is currently growing
let pointerGrowing = [false, false, false, false];

// Pointer settings
let growthSpeed = 1.5;
let maxPointerRatio = 0.38;

// Region colors
let regionColors = [
  "#F8D7E8", // HOME - pink
  "#D7E8F8", // SCHOOL - blue
  "#DDF0D7", // GYM - green
  "#F7E7B5"  // OUTDOOR - yellow
];

// Region names
let regionNames = [
  "HOME",
  "SCHOOL",
  "GYM",
  "OUTDOOR"
];

function setup() {
  createCanvas(240, 135);
  
  // Make the canvas fit the browser window
  pixelDensity(1);
  
  textFont("Arial");
}

function draw() {
  background(255);

  drawRegions();
  updatePointers();
  drawAllPointers();
  drawActiveRegion();
}

// =====================================
// Draw four regions
// =====================================

function drawRegions() {
  let halfW = width / 2;
  let halfH = height / 2;

  // HOME
  fill(regionColors[0]);
  noStroke();
  rect(0, 0, halfW, halfH);

  // SCHOOL
  fill(regionColors[1]);
  rect(halfW, 0, halfW, halfH);

  // GYM
  fill(regionColors[2]);
  rect(0, halfH, halfW, halfH);

  // OUTDOOR
  fill(regionColors[3]);
  rect(halfW, halfH, halfW, halfH);

  // Dividing lines
  stroke(255);
  strokeWeight(1);

  line(halfW, 0, halfW, height);
  line(0, halfH, width, halfH);

  // Region labels
  noStroke();
  fill(60);
  textAlign(CENTER, CENTER);
  textSize(9);

  text("HOME", halfW * 0.5, halfH * 0.25);
  text("SCHOOL", halfW * 1.5, halfH * 0.25);
  text("GYM", halfW * 0.5, halfH * 1.25);
  text("OUTDOOR", halfW * 1.5, halfH * 1.25);
}

// =====================================
// Update pointer lengths
// =====================================

function updatePointers() {
  let maxPointerLength = min(width, height) * maxPointerRatio;

  for (let i = 0; i < 4; i++) {

    if (pointerGrowing[i]) {
      pointerLengths[i] += growthSpeed;

      // Stop automatically at maximum length
      if (pointerLengths[i] >= maxPointerLength) {
        pointerLengths[i] = maxPointerLength;
        pointerGrowing[i] = false;
      }
    }
  }
}

// =====================================
// Draw all four pointers
// =====================================

function drawAllPointers() {

  // HOME
  drawPointer(
    0,
    225
  );

  // SCHOOL
  drawPointer(
    1,
    315
  );

  // GYM
  drawPointer(
    2,
    135
  );

  // OUTDOOR
  drawPointer(
    3,
    45
  );
}

// =====================================
// Draw one pointer
// =====================================

function drawPointer(region, angle) {

  let halfW = width / 2;
  let halfH = height / 2;

  let centers = [
    {
      x: halfW * 0.5,
      y: halfH * 0.5
    },
    {
      x: halfW * 1.5,
      y: halfH * 0.5
    },
    {
      x: halfW * 0.5,
      y: halfH * 1.5
    },
    {
      x: halfW * 1.5,
      y: halfH * 1.5
    }
  ];

  let centerX = centers[region].x;
  let centerY = centers[region].y;

  let length = pointerLengths[region];

  // Convert degrees to radians
  let radians = angle * PI / 180;

  let endX = centerX + cos(radians) * length;
  let endY = centerY + sin(radians) * length;

  // Pointer
  stroke(40);
  strokeWeight(2);
  line(centerX, centerY, endX, endY);

  // Small circle at pointer origin
  noStroke();
  fill(40);
  circle(centerX, centerY, 4);
}

// =====================================
// Highlight currently selected region
// =====================================

function drawActiveRegion() {

  let halfW = width / 2;
  let halfH = height / 2;

  let x = 0;
  let y = 0;

  if (activeRegion === 1) {
    x = 0;
    y = 0;
  }

  if (activeRegion === 2) {
    x = halfW;
    y = 0;
  }

  if (activeRegion === 3) {
    x = 0;
    y = halfH;
  }

  if (activeRegion === 4) {
    x = halfW;
    y = halfH;
  }

  noFill();
  stroke(255, 255, 255);
  strokeWeight(2);

  rect(x + 1, y + 1, halfW - 2, halfH - 2);
}

// =====================================
// Keyboard controls
// =====================================

function keyPressed() {

  // Select region
  if (key === "1") {
    activeRegion = 1;
  }

  if (key === "2") {
    activeRegion = 2;
  }

  if (key === "3") {
    activeRegion = 3;
  }

  if (key === "4") {
    activeRegion = 4;
  }

  // Start / continue pointer
  if (key === "q" || key === "Q") {

    let index = activeRegion - 1;

    pointerGrowing[index] = true;
  }

  // Stop pointer
  if (key === "w" || key === "W") {

    let index = activeRegion - 1;

    pointerGrowing[index] = false;
  }
}
