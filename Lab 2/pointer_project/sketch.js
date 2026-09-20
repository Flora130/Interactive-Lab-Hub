// ==========================================
// PiTFT Pointer Interaction
// Raspberry Pi + Adafruit Mini PiTFT
// Screen: 240 x 135
// ==========================================

// Currently selected region
let activeRegion = 1;

// Each region has its own pointer length
let pointerLengths = [0, 0, 0, 0];

// Whether each pointer is growing
let pointerGrowing = [false, false, false, false];

// Pointer settings
let growthSpeed = 1.5;
let maxPointerRatio = 0.38;


// ==========================================
// Region settings
// ==========================================

let regionColors = [
  "#F8D7E8", // HOME - pink
  "#D7E8F8", // SCHOOL - blue
  "#DDF0D7", // GYM - green
  "#F7E7B5"  // OUTDOOR - yellow
];

let regionNames = [
  "HOME",
  "SCHOOL",
  "GYM",
  "OUTDOOR"
];


// ==========================================
// Setup
// ==========================================

function setup() {

  // PiTFT resolution
  createCanvas(240, 135);

  // Important for small Raspberry Pi display
  pixelDensity(1);

  // Simple font
  textFont("Arial");

  // Start with no pointer growing
  for (let i = 0; i < 4; i++) {
    pointerGrowing[i] = false;
  }
}


// ==========================================
// Main draw loop
// ==========================================

function draw() {

  background(255);

  // Draw four areas
  drawRegions();

  // Update pointer lengths
  updatePointers();

  // Draw all pointers
  drawAllPointers();

  // Highlight currently selected area
  drawActiveRegion();
}


// ==========================================
// Draw four regions
// ==========================================

function drawRegions() {

  let halfW = width / 2;
  let halfH = height / 2;

  noStroke();

  // HOME
  fill(regionColors[0]);
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


  // Center dividing lines
  stroke(255);
  strokeWeight(1);

  line(halfW, 0, halfW, height);
  line(0, halfH, width, halfH);


  // Region labels
  noStroke();
  fill(60);

  textAlign(CENTER, CENTER);
  textSize(9);

  text("HOME",  halfW * 0.5, halfH * 0.25);
  text("SCHOOL", halfW * 1.5, halfH * 0.25);
  text("GYM",   halfW * 0.5, halfH * 1.25);
  text("OUTDOOR", halfW * 1.5, halfH * 1.25);
}


// ==========================================
// Update pointers
// ==========================================

function updatePointers() {

  let maxPointerLength =
    min(width, height) * maxPointerRatio;

  for (let i = 0; i < 4; i++) {

    if (pointerGrowing[i]) {

      pointerLengths[i] += growthSpeed;

      // Stop when maximum length is reached
      if (pointerLengths[i] >= maxPointerLength) {

        pointerLengths[i] = maxPointerLength;

        pointerGrowing[i] = false;
      }
    }
  }
}


// ==========================================
// Draw all four pointers
// ==========================================

function drawAllPointers() {

  // HOME
  drawPointer(0, 225);

  // SCHOOL
  drawPointer(1, 315);

  // GYM
  drawPointer(2, 135);

  // OUTDOOR
  drawPointer(3, 45);
}


// ==========================================
// Draw individual pointer
// ==========================================

function drawPointer(region, angle) {

  let halfW = width / 2;
  let halfH = height / 2;

  // Center of each region
  let centers = [

    // HOME
    {
      x: halfW * 0.5,
      y: halfH * 0.5
    },

    // SCHOOL
    {
      x: halfW * 1.5,
      y: halfH * 0.5
    },

    // GYM
    {
      x: halfW * 0.5,
      y: halfH * 1.5
    },

    // OUTDOOR
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


  // Calculate pointer endpoint
  let endX =
    centerX + cos(radians) * length;

  let endY =
    centerY + sin(radians) * length;


  // Pointer line
  stroke(40);
  strokeWeight(2);

  line(
    centerX,
    centerY,
    endX,
    endY
  );


  // Pointer center
  noStroke();
  fill(40);

  circle(
    centerX,
    centerY,
    4
  );
}


// ==========================================
// Highlight active region
// ==========================================

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


  // White border around active region
  noFill();

  stroke(255);
  strokeWeight(2);

  rect(
    x + 1,
    y + 1,
    halfW - 2,
    halfH - 2
  );
}


// ==========================================
// Keyboard controls
// ==========================================
//
// 1 = HOME
// 2 = SCHOOL
// 3 = GYM
// 4 = OUTDOOR
//
// Q = start growing
// W = stop growing
//
// These will later be replaced by
// the two PiTFT physical buttons.
// ==========================================

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


  // Start pointer

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
