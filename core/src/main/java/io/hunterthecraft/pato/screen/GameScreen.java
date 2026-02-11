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
    private SpriteBatch worldBatch;
    private SpriteBatch uiBatch;
    private OrthographicCamera worldCamera;
    private OrthographicCamera uiCamera;
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
            worldBatch = new SpriteBatch();
            uiBatch = new SpriteBatch();            
            worldCamera = new OrthographicCamera();
            viewport = new ScreenViewport(worldCamera);
            viewport.update(Gdx.graphics.getWidth(), Gdx.graphics.getHeight(), true);

            uiCamera = new OrthographicCamera();
            uiCamera.setToOrtho(false, Gdx.graphics.getWidth(), Gdx.graphics.getHeight());

            worldRenderer = new WorldRenderer(worldBatch);
            uiRenderer = new UiRenderer(uiBatch);
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
            worldCamera.position.set(panOffsetX, panOffsetY, 0);
            worldCamera.zoom = zoom;
            worldCamera.update();

            ScreenUtils.clear(0.1f, 0.1f, 0.15f, 1);

            // ========== RENDERIZA MUNDO ==========
            worldBatch.begin();
            worldBatch.setProjectionMatrix(worldCamera.combined);
            worldRenderer.render(worldCamera.position.x, worldCamera.position.y, zoom);
            worldBatch.end();

            // ========== RENDERIZA UI (FIXA) ==========
            uiBatch.begin();
            uiBatch.setProjectionMatrix(uiCamera.combined);
            
            uiRenderer.drawPauseButton();
            
            if (popupOpen && selectedTile != null) {
                uiRenderer.drawTilePopup(selectedX, selectedY, selectedTile);
            }
            
            if (pauseMenuOpen && !settingsOpen) {
                uiRenderer.drawPauseMenu();
                
                // ✅ DETECÇÃO DE CLIQUE NOS BOTÕES DO MENU
                if (Gdx.input.justTouched()) {
                    float touchX = Gdx.input.getX();                    float touchY = Gdx.graphics.getHeight() - Gdx.input.getY(); // inverte Y
                    
                    // Botão "Continuar" (y: -120 a -80)
                    if (touchY > Gdx.graphics.getHeight() - 120 && touchY < Gdx.graphics.getHeight() - 80) {
                        pauseMenuOpen = false;
                        inputController.setPauseMenuOpen(false);
                    }
                    // Botão "Menu Principal" (y: -160 a -120)
                    else if (touchY > Gdx.graphics.getHeight() - 160 && touchY < Gdx.graphics.getHeight() - 120) {
                        game.setScreen(new MainMenuScreen(game));
                    }
                    // Botão "Configurações" (y: -200 a -160)
                    else if (touchY > Gdx.graphics.getHeight() - 200 && touchY < Gdx.graphics.getHeight() - 160) {
                        settingsOpen = true;
                    }
                    // Botão "Sair" (y: -240 a -200)
                    else if (touchY > Gdx.graphics.getHeight() - 240 && touchY < Gdx.graphics.getHeight() - 200) {
                        Gdx.app.exit();
                    }
                }
            } else if (settingsOpen) {
                uiRenderer.drawSettingsMenu(
                    inputController.isInvertScrollY(),
                    inputController.isInvertPinch(),
                    inputController.getPinchSensitivity(),
                    inputController.getScrollSensitivity()
                );
                
                // ✅ DETECÇÃO DE CLIQUE NO BOTÃO "VOLTAR"
                if (Gdx.input.justTouched()) {
                    float touchX = Gdx.input.getX();
                    float touchY = Gdx.graphics.getHeight() - Gdx.input.getY();
                    
                    // Botão "Voltar" (y: 100 a 140)
                    if (touchY > 100 && touchY < 140) {
                        settingsOpen = false;
                    }
                }
            }
            uiBatch.end();
        } catch (Exception e) {
            Gdx.app.error("GameScreen", "Erro na renderização", e);
            game.setScreen(new BugCenterScreen(game, "Erro de renderização:\n" + e.toString()));
        }
    }

    @Override
    public void onTileTapped(int screenX, int screenY) {
        if (pauseMenuOpen || settingsOpen) return; // ← Ignora cliques no mundo quando menu aberto
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
        if (!pauseMenuOpen && !settingsOpen) {
            panOffsetX += deltaX * zoom;
            panOffsetY += deltaY * zoom;
        }
    }

    @Override
    public void onZoom(float delta) {
        if (!pauseMenuOpen && !settingsOpen) {
            zoom += delta;
            zoom = Math.max(0.5f, Math.min(3.0f, zoom));
        }
    }

    @Override
    public void onPauseButtonTapped() {
        pauseMenuOpen = true;
        inputController.setPauseMenuOpen(true);    }

    @Override
    public void resize(int width, int height) {
        viewport.update(width, height, true);
        uiCamera.setToOrtho(false, width, height);
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
        if (worldBatch != null) worldBatch.dispose();
        if (uiBatch != null) uiBatch.dispose();
    }
}