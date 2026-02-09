// core/src/io/hunterthecraft/pato/screen/GameScreen.java
package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.OrthographicCamera;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.input.GestureDetector;
import com.badlogic.gdx.math.Vector2;
import com.badlogic.gdx.utils.ScreenUtils;
import com.badlogic.gdx.utils.viewport.ScreenViewport;
import io.hunterthecraft.pato.PatoGame;
import io.hunterthecraft.pato.controller.InputController;
import io.hunterthecraft.pato.data.TileType;
import io.hunterthecraft.pato.model.Chunk;
import io.hunterthecraft.pato.model.ChunkManager;
import io.hunterthecraft.pato.renderer.UiRenderer;
import io.hunterthecraft.pato.renderer.WorldRenderer;

public class GameScreen implements Screen, InputController.InputListener {
    private PatoGame game;
    private SpriteBatch batch;
    private OrthographicCamera camera;
    private ScreenViewport viewport;

    private WorldRenderer worldRenderer;
    private UiRenderer uiRenderer;
    private InputController inputController;

    private float zoom = 1.0f;
    private float panOffsetX = 0, panOffsetY = 0;

    private TileType selectedTile = null;
    private int selectedX = -1, selectedY = -1;
    private boolean popupOpen = false;

    private boolean pauseMenuOpen = false;
    private boolean settingsOpen = false;

    public GameScreen(PatoGame game) {
        this.game = game;
    }

    @Override
    public void show() {
        try {
            batch = new SpriteBatch();
            camera = new OrthographicCamera();
            viewport = new ScreenViewport(camera);
            viewport.update(Gdx.graphics.getWidth(), Gdx.graphics.getHeight(), true);
            worldRenderer = new WorldRenderer(batch);
            uiRenderer = new UiRenderer(batch);
            inputController = new InputController(this);

            Gdx.input.setInputProcessor(new GestureDetector(inputController));
        } catch (Exception e) {
            Gdx.app.error("GameScreen", "Erro na inicialização", e);
            game.setScreen(new BugCenterScreen(game, "Falha ao iniciar jogo:\n" + e.toString()));
        }
    }

    @Override
    public void render(float delta) {
        try {
            camera.position.set(panOffsetX, panOffsetY, 0);
            camera.zoom = zoom;
            camera.update();

            ScreenUtils.clear(0.1f, 0.1f, 0.15f, 1);

            // Renderiza MUNDO (com câmera)
            batch.begin();
            batch.setProjectionMatrix(camera.combined);
            worldRenderer.render(camera.position.x, camera.position.y, zoom);
            batch.end();

            // Renderiza UI (coordenadas de tela fixas)
            batch.begin();
            batch.setProjectionMatrix(new OrthographicCamera().combined);
            uiRenderer.drawPauseButton();
            
            if (popupOpen && selectedTile != null) {
                uiRenderer.drawTilePopup(selectedX, selectedY, selectedTile);
            }
            
            if (pauseMenuOpen && !settingsOpen) {
                uiRenderer.drawPauseMenu();
            } else if (settingsOpen) {
                uiRenderer.drawSettingsMenu(
                    inputController.isInvertScrollY(),
                    inputController.isInvertPinch(),
                    inputController.getPinchSensitivity(),
                    inputController.getScrollSensitivity()
                );
            }
            batch.end();

            inputController.setPauseMenuOpen(pauseMenuOpen);
            inputController.setSettingsOpen(settingsOpen);        } catch (Exception e) {
            Gdx.app.error("GameScreen", "Erro na renderização", e);
            game.setScreen(new BugCenterScreen(game, "Erro de renderização:\n" + e.toString()));
        }
    }

    @Override
    public void onTileTapped(int screenX, int screenY) {
        Vector2 screenPos = new Vector2(screenX, screenY);
        Vector2 worldPos = viewport.unproject(screenPos);
        
        int tileX = (int) (worldPos.x / 128);
        int tileY = (int) (worldPos.y / 128);

        if (tileX < 0 || tileY < 0) return;

        int chunkX = ChunkManager.getChunkX(tileX);
        int chunkY = ChunkManager.getChunkY(tileY);
        int localX = tileX - chunkX * Chunk.SIZE;
        int localY = tileY - chunkY * Chunk.SIZE;

        if (localX < 0 || localX >= Chunk.SIZE || localY < 0 || localY >= Chunk.SIZE) return;

        if (popupOpen && selectedX == tileX && selectedY == tileY) {
            popupOpen = false;
        } else {
            selectedX = tileX;
            selectedY = tileY;
            try {
                Chunk chunk = worldRenderer.getChunkManager().getChunk(chunkX, chunkY);
                selectedTile = chunk.getTile(localX, localY);
                popupOpen = true;
            } catch (Exception e) {
                Gdx.app.error("GameScreen", "Erro ao obter chunk", e);
            }
        }
    }

    @Override
    public void onPan(float deltaX, float deltaY) {
        panOffsetX += deltaX * zoom;
        panOffsetY += deltaY * zoom;
    }

    @Override
    public void onZoom(float delta) {
        zoom += delta;
        zoom = Math.max(0.5f, Math.min(3.0f, zoom));
    }
    @Override
    public void onPauseButtonTapped() {
        pauseMenuOpen = true;
    }

    @Override
    public void resize(int width, int height) {
        viewport.update(width, height, true);
    }

    @Override
    public void pause() {}
    @Override
    public void resume() {}
    @Override
    public void hide() {}

    @Override
    public void dispose() {
        if (worldRenderer != null) worldRenderer.dispose();
        if (uiRenderer != null) uiRenderer.dispose();
        if (batch != null) batch.dispose();
    }
}