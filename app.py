import streamlit as st
import base64

st.title("alice site")
st.header("Save the Forest")

description = """
This game is based on SDGs 15 which is, Life on Land.   
The main idea of the game is to save the forest and make the air quality better for humans and animals living on land. 
The player will have to destroy the factories instead of cutting down the trees, when all the factories change to clear, you win the game.  """
st.write(description)


# The player had to collect trees to plant, however if you get a factory 3 times, you get eliminated. 

# Function to convert an image file to a base64 encoded string.
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


# Paths to the image files.
image_path_1 = "1.png"  # Path to the first image.
image_path_2 = "2.png"  # Path to the second image.
image_path_3 = "3.png"
image_path_4 = "4.png"
plane_image_path = "plane.png"
clear_image_path = "clear.png"

# Encode both images to base64 strings.
encoded_image_1 = get_base64_image(image_path_1)
encoded_image_2 = get_base64_image(image_path_2)
encoded_image_3 = get_base64_image(image_path_3)
encoded_plane_image = get_base64_image(plane_image_path)
encoded_clear_image = get_base64_image(clear_image_path)
encoded_image_4 = get_base64_image(image_path_4)

html_code = f"""
<!DOCTYPE html>
<html>
<head>
  <style>
    .container {{
      position: relative;
      display: inline-block;
    }}
    .clickable-area {{
  position: absolute;
  top: 203px;
  left: 262px;
  width: 72px;
  height: 23px;
  cursor: pointer;
  background-color: transparent;
  border: none;
  z-index: 10;
}}

    .red-box {{
  position: absolute;
  width: 40px;
  height: 40px;
  background-color: transparent; 
  display: none;
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  }}
    #game-image {{
      width: 600px;
      cursor: pointer;
    }}
    #plane {{
      position: absolute;
      top: 100px;
      left: 200px;
      width: 100px;
      display: none;
      pointer-events: none;
      transition: top 0.1s, left 0.1s;
    }}
    .red-box {{
  position: absolute;
  width: 40px;
  height: 40px;
  background-color: transparent; 
  display: none;
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  }}
  </style>
</head>
<body tabindex="0">
  <div class="container" onclick="handleImageClick()">
    <img id="game-image" src="data:image/png;base64,{encoded_image_1}" alt="Game Image">
    <img id="plane" src="data:image/png;base64,{encoded_plane_image}" alt="Plane">
    
    <!-- Red Boxes -->
<div id="box1" class="red-box" style="top: 8px; left: 515px; width: 90px; height: 85px;"></div>
<div id="box2" class="red-box" style="top: -5px; left: 100px; width: 80px; height: 80px;"></div>
<div id="box3" class="red-box" style="top: 135px; left: -10px; width: 80px; height: 80px;"></div>
<div id="box4" class="red-box" style="top: 155px; left: 180px; width: 50px; height: 40px;"></div>
<div id="box5" class="red-box" style="top: 265px; left: 225px; width: 80px; height: 80px;"></div>
<div id="box6" class="red-box" style="top: 190px; left: 515px; width: 80px; height: 80px;"></div>

    <div id="clickableArea" class="clickable-area" onclick="handleBoxClick(event)"></div>
  </div>

  <script>
    let currentStage = 1;

    function isColliding(a, b) {{
    const rect1 = a.getBoundingClientRect();
    const rect2 = b.getBoundingClientRect();
    return !(
      rect1.right < rect2.left ||
      rect1.left > rect2.right ||
      rect1.bottom < rect2.top ||
      rect1.top > rect2.bottom
    );
  }}

    function handleBoxClick(event) {{
      event.stopPropagation();
      document.getElementById("game-image").src = "data:image/png;base64,{encoded_image_2}";
      document.getElementById("clickableArea").style.display = "none";
      currentStage = 2;
    }}

    function handleImageClick() {{
      if (currentStage === 2) {{
        document.getElementById("game-image").src = "data:image/png;base64,{encoded_image_3}";
        const plane = document.getElementById("plane");
        plane.style.display = "block";
        currentStage = 3;

        // Reset plane position
        plane.style.top = "250px";
        plane.style.left = "0px";

        // Show red boxes
        for (let i = 1; i <= 6; i++) {{
          document.getElementById("box" + i).style.display = "block";
        }}

        document.body.focus();
      }}
    }}

    document.body.addEventListener('keydown', function(event) {{
  const plane = document.getElementById("plane");
  const gameImage = document.getElementById("game-image");
  if (currentStage !== 3 || plane.style.display === "none") return;

  let top = parseInt(plane.style.top);
  let left = parseInt(plane.style.left);
  const step = 10;

  const maxLeft = gameImage.clientWidth - plane.clientWidth;
  const maxTop = gameImage.clientHeight - plane.clientHeight;

  const clearImage = "data:image/png;base64,{encoded_clear_image}";

  switch(event.key) {{
    case 'ArrowUp':
      top = Math.max(0, top - step);
      break;
    case 'ArrowDown':
      top = Math.min(maxTop, top + step);
      break;
    case 'ArrowLeft':
      left = Math.max(0, left - step);
      break;
    case 'ArrowRight':
      left = Math.min(maxLeft, left + step);
      break;
    default:
      return;
  }}

  plane.style.top = top + "px";
  plane.style.left = left + "px";
  event.preventDefault();

  for (let i = 1; i <= 6; i++) {{
  const box = document.getElementById("box" + i);
  if (box && box.style.display !== "none" && isColliding(plane, box)) {{
    box.style.backgroundColor = "transparent";
    box.style.backgroundImage = `url('${{clearImage}}')`;
    box.setAttribute("data-cleared", "true");
  }}
}}

// Check if all boxes are cleared
let allCleared = true;
for (let i = 1; i <= 6; i++) {{
  const box = document.getElementById("box" + i);
  if (box && box.style.display !== "none") {{
    if (box.getAttribute("data-cleared") !== "true") {{
      allCleared = false;
      break;
    }}
  }}
}}

if (allCleared) {{
  setTimeout(() => {{
    document.getElementById("game-image").src = "data:image/png;base64,{encoded_image_4}";

    // Hide all boxes after the image changes
    for (let i = 1; i <= 6; i++) {{
      const box = document.getElementById("box" + i);
      if (box) {{
        box.style.display = "none";
      }}
    }}

  }}, 3000);
}}


}});

  </script>
</body>
</html>
"""

# Render the custom HTML code within the Streamlit app.
st.components.v1.html(html_code, height=700)
