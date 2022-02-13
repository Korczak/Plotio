export default abstract class CanvasDrawer {
  public static drawSquarePoint(
    context: any,
    x: number,
    y: number,
    color: string,
    size: number
  ) {
    if (color == null) {
      color = "#000";
    }
    if (size == null) {
      size = 5;
    }

    const radius = 0.5 * size;

    // to increase smoothing for numbers with decimal part
    const pointX = Math.round(x - radius);
    const pointY = Math.round(y - radius);

    context.beginPath();
    context.fillStyle = color;
    context.fillRect(pointX, pointY, size, size);
    context.fill();
  }
}
