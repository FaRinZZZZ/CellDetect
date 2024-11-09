import numpy as np
import cv2

# Load and convert image to grayscale
bmp = cv2.imread('asset/pic/bloodcell.bmp', cv2.IMREAD_GRAYSCALE)
cv2.imwrite('asset/pic/BloodGray.png', bmp)
img = cv2.imread('asset/pic/BloodGray.png')
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Create a named window for trackbars
cv2.namedWindow('Controls')

# Initial HSV range and contour area threshold values
initial_values = {'H Lower': 0, 'H Upper': 180, 'S Lower': 0, 'S Upper': 255, 'V Lower': 0, 'V Upper': 75, 'Contour Area': 205}

# Define a callback function for the trackbars
def nothing(x):
    pass

# Create trackbars for lower and upper HSV bounds
cv2.createTrackbar('H Lower', 'Controls', initial_values['H Lower'], 180, nothing)
cv2.createTrackbar('H Upper', 'Controls', initial_values['H Upper'], 180, nothing)
cv2.createTrackbar('S Lower', 'Controls', initial_values['S Lower'], 255, nothing)
cv2.createTrackbar('S Upper', 'Controls', initial_values['S Upper'], 255, nothing)
cv2.createTrackbar('V Lower', 'Controls', initial_values['V Lower'], 255, nothing)
cv2.createTrackbar('V Upper', 'Controls', initial_values['V Upper'], 255, nothing)
cv2.createTrackbar('Contour Area', 'Controls', initial_values['Contour Area'], 1000, nothing)

while True:
    # Get current positions of trackbars
    h_lower = cv2.getTrackbarPos('H Lower', 'Controls')
    h_upper = cv2.getTrackbarPos('H Upper', 'Controls')
    s_lower = cv2.getTrackbarPos('S Lower', 'Controls')
    s_upper = cv2.getTrackbarPos('S Upper', 'Controls')
    v_lower = cv2.getTrackbarPos('V Lower', 'Controls')
    v_upper = cv2.getTrackbarPos('V Upper', 'Controls')
    contour_area_threshold = cv2.getTrackbarPos('Contour Area', 'Controls')

    # Define HSV range based on trackbar positions
    lower_range = (h_lower, s_lower, v_lower)
    upper_range = (h_upper, s_upper, v_upper)

    # Create mask and apply it
    mask = cv2.inRange(hsv_img, lower_range, upper_range)
    result = img.copy()  # Copy of the original image for drawing contours in color

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Count and draw contours that meet the area threshold
    cell_count = 0
    for cnt in contours:
        if cv2.contourArea(cnt) >= contour_area_threshold:
            cv2.drawContours(result, [cnt], -1, (0, 0, 255), 2)  # Draw contours in red
            cell_count += 1

    # Prepare images for display
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Original in grayscale
    color_result = result  # Contours drawn on original image in color
    mask_colored = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  # Convert mask to BGR for consistent stacking

    # Stack images horizontally for single window display
    combined_display = np.hstack((cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR), mask_colored, color_result))

    # Display cell count on the console
    print(f'Cell count: {cell_count}', end='\r')

    # Show combined image
    cv2.imshow('Detection Results', combined_display)

    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up windows
cv2.destroyAllWindows()