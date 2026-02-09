// core/src/io/hunterthecraft/pato/controller/InputController.java
package io.hunterthecraft.pato.controller;

import com.badlogic.gdx.input.GestureDetector;
import com.badlogic.gdx.math.Vector2;

public class InputController implements GestureDetector.GestureListener {
    public interface InputListener {
        void onTileTapped(int tileX, int tileY);
        void onPan(float deltaX, float deltaY);
        void onZoom(float delta);
        void onPauseButtonTapped();
    }

    private InputListener listener;
    private boolean invertScrollY = false;
    private boolean invertPinch = false;
    private float pinchSensitivity = 0.005f;
    private float scrollSensitivity = 1.0f;
    private boolean pauseMenuOpen = false;
    private boolean settingsOpen = false;

    public InputController(InputListener listener) {
        this.listener = listener;
    }

    public void setPauseMenuOpen(boolean pauseMenuOpen) {
        this.pauseMenuOpen = pauseMenuOpen;
    }

    public void setSettingsOpen(boolean settingsOpen) {
        this.settingsOpen = settingsOpen;
    }

    // Getters/Setters para configurações
    public boolean isInvertScrollY() { return invertScrollY; }
    public void setInvertScrollY(boolean invertScrollY) { this.invertScrollY = invertScrollY; }

    public boolean isInvertPinch() { return invertPinch; }
    public void setInvertPinch(boolean invertPinch) { this.invertPinch = invertPinch; }

    public float getPinchSensitivity() { return pinchSensitivity; }
    public void setPinchSensitivity(float pinchSensitivity) { this.pinchSensitivity = pinchSensitivity; }

    public float getScrollSensitivity() { return scrollSensitivity; }
    public void setScrollSensitivity(float scrollSensitivity) { this.scrollSensitivity = scrollSensitivity; }

    @Override
    public boolean touchDown(float x, float y, int pointer, int button) {
        // Verifica clique no botão de pausa (canto inferior direito)        if (!pauseMenuOpen && !settingsOpen) {
            if (x > Gdx.graphics.getWidth() - 60 && y > Gdx.graphics.getHeight() - 60) {
                listener.onPauseButtonTapped();
                return true;
            }
        }
        return false;
    }

    @Override
    public boolean tap(float x, float y, int count, int button) {
        if (!pauseMenu, !settingsOpen) {
            // Conversão para coordenadas do mundo deve ser feita pelo listener
            listener.onTileTapped((int)x, (int)y);
        }
        return false;
    }

    @Override
    public boolean longPress(float x, float y) { return false; }

    @Override
    public boolean fling(float velocityX, float velocityY, int button) { return false; }

    @Override
    public boolean pan(float x, float y, float deltaX, float deltaY) {
        if (!pauseMenuOpen && !settingsOpen) {
            float finalDeltaY = invertScrollY ? -deltaY : deltaY;
            listener.onPan(-deltaX * scrollSensitivity, finalDeltaY * scrollSensitivity);
        }
        return false;
    }

    @Override
    public boolean panStop(float x, float y, int pointer, int button) { return false; }

    @Override
    public boolean zoom(float initialDistance, float distance) {
        if (!pauseMenuOpen && !settingsOpen) {
            float delta = distance - initialDistance;
            if (invertPinch) delta = -delta;
            listener.onZoom(delta * pinchSensitivity);
        }
        return false;
    }

    @Override
    public boolean pinch(Vector2 initialPointer1, Vector2 initialPointer2, Vector2 pointer1, Vector2 pointer2) { return false; }

    @Override    public void pinchStop() {}
}