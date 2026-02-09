// core/src/io/hunterthecraft/pato/screen/GameScreen.java
package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.OrthographicCamera;
import com.badlogic.gdx.graphics.Pixmap;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.graphics.g2d.GlyphLayout;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.input.GestureDetector;
import com.badlogic.gdx.math.Vector2;
import com.badlogic.gdx.utils.ScreenUtils;
import com.badlogic.gdx.utils.viewport.ScreenViewport;
import io.hunterthecraft.pato.PatoGame;
import io.hunterthecraft.pato.data.TileType;
import io.hunterthecraft.pato.model.Chunk;
import io.hunterthecraft.pato.model.ChunkManager;

public class GameScreen implements Screen, GestureDetector.GestureListener {
    private PatoGame game;
    private SpriteBatch batch;
    private BitmapFont font;
    private GlyphLayout layout;
    private Texture[] tileTextures;
    private Texture whitePixel;

    private OrthographicCamera camera;
    private ScreenViewport viewport;
    private float zoom = 1.0f;
    private Vector2 panOffset = new Vector2();

    private ChunkManager chunkManager = new ChunkManager();
    private static final int TILE_SIZE = 128;

    private TileType selectedTile = null;
    private int selectedX = -1, selectedY = -1;
    private boolean popupOpen = false;

    private boolean pauseMenuOpen = false;
    private boolean settingsOpen = false;

    // Controles de input
    private boolean invertScrollY = false;
    private boolean invertPinch = false;
    private float pinchSensitivity = 0.005f;
    private float scrollSensitivity = 1.0f;
    public GameScreen(PatoGame game) {
        this.game = game;
    }

    @Override
    public void show() {
        try {
            batch = new SpriteBatch();
            font = new BitmapFont();
            font.getData().setScale(1.0f);
            layout = new GlyphLayout();

            Pixmap pixmap = new Pixmap(1, 1, Pixmap.Format.RGBA8888);
            pixmap.setColor(Color.WHITE);
            pixmap.fill();
            whitePixel = new Texture(pixmap);
            pixmap.dispose();

            camera = new OrthographicCamera();
            viewport = new ScreenViewport(camera);
            viewport.update(Gdx.graphics.getWidth(), Gdx.graphics.getHeight(), true);

            tileTextures = new Texture[2];
            tileTextures[0] = new Texture("tiles/debug_amazonia.png");
            tileTextures[1] = new Texture("tiles/debug_cerrado.png");

            GestureDetector detector = new GestureDetector(this);
            Gdx.input.setInputProcessor(detector);
        } catch (Exception e) {
            Gdx.app.error("GameScreen", "Erro na inicialização", e);
            game.setScreen(new BugCenterScreen(game, "Falha ao iniciar jogo:\n" + e.toString()));
        }
    }

    @Override
    public void render(float delta) {
        try {
            camera.position.set(panOffset.x, panOffset.y, 0);
            camera.zoom = zoom;
            camera.update();
            batch.setProjectionMatrix(camera.combined);

            ScreenUtils.clear(0.1f, 0.1f, 0.15f, 1);
            batch.begin();

            renderChunks();

            if (popupOpen && selectedTile != null) {
                float px = selectedX * TILE_SIZE;
                float py = selectedY * TILE_SIZE + TILE_SIZE;
                batch.setColor(0, 0, 0, 0.7f);
                batch.draw(whitePixel, px, py, 200, 100);
                batch.setColor(1, 1, 1, 1);

                font.setColor(Color.WHITE);
                layout.setText(font, "Bioma: " + selectedTile.toString());
                font.draw(batch, layout, px + 10, py + 80);

                layout.setText(font, String.format("Coord: (%d, %d)", selectedX, selectedY));
                font.draw(batch, layout, px + 10, py + 60);

                layout.setText(font, "✕");
                font.draw(batch, layout, px + 180, py + 90);
            }

            drawPauseButton();

            if (pauseMenuOpen && !settingsOpen) {
                drawPauseMenu();
            } else if (settingsOpen) {
                drawSettingsMenu();
            }

            batch.end();
        } catch (Exception e) {
            Gdx.app.error("GameScreen", "Erro na renderização", e);
            game.setScreen(new BugCenterScreen(game, "Erro de renderização:\n" + e.toString()));
        }
    }

    private void renderChunks() {
        try {
            // Calcula posição central em coordenadas de tile
            int centerTileX = (int) (camera.position.x / TILE_SIZE);
            int centerTileY = (int) (camera.position.y / TILE_SIZE);
            
            // Converte para coordenadas de chunk
            int centerChunkX = ChunkManager.getChunkX(centerTileX);
            int centerChunkY = ChunkManager.getChunkY(centerTileY);

            int radius = 2;
            for (int cy = centerChunkY - radius; cy <= centerChunkY + radius; cy++) {
                for (int cx = centerChunkX - radius; cx <= centerChunkX + radius; cx++) {
                    Chunk chunk = chunkManager.getChunk(cx, cy);
                    for (int y = 0; y < Chunk.SIZE; y++) {
                        for (int x = 0; x < Chunk.SIZE; x++) {
                            TileType tile = chunk.getTile(x, y);
                            int globalX = cx * Chunk.SIZE + x;
                            int globalY = cy * Chunk.SIZE + y;                            Texture tex = (tile == TileType.AMAZONIA) ? tileTextures[0] : tileTextures[1];
                            batch.draw(tex, globalX * TILE_SIZE, globalY * TILE_SIZE, TILE_SIZE, TILE_SIZE);
                        }
                    }
                }
            }

            chunkManager.unloadDistantChunks(centerChunkX, centerChunkY);
        } catch (Exception e) {
            Gdx.app.error("GameScreen", "Erro ao renderizar chunks", e);
            throw e;
        }
    }

    private void drawPauseButton() {
        try {
            float btnX = Gdx.graphics.getWidth() - 60;
            float btnY = Gdx.graphics.getHeight() - 60;
            batch.setColor(0.2f, 0.2f, 0.3f, 0.8f);
            batch.draw(whitePixel, btnX, btnY, 50, 50);
            batch.setColor(1, 1, 1, 1);
            font.setColor(Color.WHITE);
            layout.setText(font, "⏸");
            font.draw(batch, layout, btnX + 15, btnY + 35);
        } catch (Exception e) {
            Gdx.app.error("GameScreen", "Erro ao desenhar botão de pausa", e);
        }
    }

    private void drawPauseMenu() {
        try {
            batch.setColor(0, 0, 0, 0.6f);
            batch.draw(whitePixel, 0, 0, Gdx.graphics.getWidth(), Gdx.graphics.getHeight());
            batch.setColor(1, 1, 1, 1);

            font.setColor(Color.YELLOW);
            layout.setText(font, "PAUSA");
            font.draw(batch, layout, 100, Gdx.graphics.getHeight() - 80);

            font.setColor(Color.WHITE);
            layout.setText(font, "Continuar");
            font.draw(batch, layout, 100, Gdx.graphics.getHeight() - 120);

            layout.setText(font, "Menu Principal");
            font.draw(batch, layout, 100, Gdx.graphics.getHeight() - 160);

            layout.setText(font, "Configurações");
            font.draw(batch, layout, 100, Gdx.graphics.getHeight() - 200);

            layout.setText(font, "Sair");            font.draw(batch, layout, 100, Gdx.graphics.getHeight() - 240);

            if (Gdx.input.justTouched()) {
                float touchY = Gdx.graphics.getHeight() - Gdx.input.getY();
                if (touchY > 110 && touchY < 130) {
                    pauseMenuOpen = false;
                } else if (touchY > 150 && touchY < 170) {
                    game.setScreen(new MainMenuScreen(game));
                } else if (touchY > 190 && touchY < 210) {
                    settingsOpen = true;
                } else if (touchY > 230 && touchY < 250) {
                    Gdx.app.exit();
                }
            }
        } catch (Exception e) {
            Gdx.app.error("GameScreen", "Erro no menu de pausa", e);
        }
    }

    private void drawSettingsMenu() {
        batch.setColor(0, 0, 0, 0.7f);
        batch.draw(whitePixel, 50, 50, Gdx.graphics.getWidth() - 100, Gdx.graphics.getHeight() - 100);
        batch.setColor(1, 1, 1, 1);

        font.setColor(Color.YELLOW);
        layout.setText(font, "CONTROLES");
        font.draw(batch, layout, 100, Gdx.graphics.getHeight() - 100);

        int y = Gdx.graphics.getHeight() - 140;

        // Inverter Eixo Y (Scroll)
        font.setColor(Color.WHITE);
        String scrollText = "Inverter Eixo Y: " + (invertScrollY ? "SIM" : "NÃO");
        layout.setText(font, scrollText);
        font.draw(batch, layout, 100, y);
        if (Gdx.input.justTouched() && touchInRect(100, y - 20, 300, 30)) {
            invertScrollY = !invertScrollY;
        }
        y -= 40;

        // Inverter Pinça
        String pinchText = "Inverter Pinça: " + (invertPinch ? "SIM" : "NÃO");
        layout.setText(font, pinchText);
        font.draw(batch, layout, 100, y);
        if (Gdx.input.justTouched() && touchInRect(100, y - 20, 300, 30)) {
            invertPinch = !invertPinch;
        }
        y -= 40;

        // Sensibilidade Pinça        String pinchSensText = "Sens. Pinça: " + String.format("%.4f", pinchSensitivity);
        layout.setText(font, pinchSensText);
        font.draw(batch, layout, 100, y);
        if (Gdx.input.justTouched() && touchInRect(100, y - 20, 300, 30)) {
            pinchSensitivity = Math.max(0.001f, Math.min(0.02f, pinchSensitivity + 0.001f));
        }
        y -= 40;

        // Sensibilidade Scroll
        String scrollSensText = "Sens. Scroll: " + String.format("%.2f", scrollSensitivity);
        layout.setText(font, scrollSensText);
        font.draw(batch, layout, 100, y);
        if (Gdx.input.justTouched() && touchInRect(100, y - 20, 300, 30)) {
            scrollSensitivity = Math.max(0.5f, Math.min(3.0f, scrollSensitivity + 0.1f));
        }
        y -= 60;

        // Botão Voltar
        layout.setText(font, "Voltar");
        font.draw(batch, layout, 100, 100);
        if (Gdx.input.justTouched() && Gdx.input.getY() < 150) {
            settingsOpen = false;
        }
    }

    private boolean touchInRect(float x, float y, float width, float height) {
        float touchX = Gdx.input.getX();
        float touchY = Gdx.graphics.getHeight() - Gdx.input.getY();
        return touchX >= x && touchX <= x + width &&
               touchY >= y && touchY <= y + height;
    }

    @Override
    public boolean touchDown(float x, float y, int pointer, int button) {
        return false;
    }

    @Override
    public boolean tap(float x, float y, int count, int button) {
        if (pauseMenuOpen || settingsOpen) return false;

        try {
            Vector2 screenPos = new Vector2(x, y);
            Vector2 worldPos = viewport.unproject(screenPos);

            int tileX = (int) (worldPos.x / TILE_SIZE);
            int tileY = (int) (worldPos.y / TILE_SIZE);

            // Calcula chunk e coordenadas locais corretamente
            int chunkX = ChunkManager.getChunkX(tileX);            int chunkY = ChunkManager.getChunkY(tileY);
            int localX = tileX - chunkX * Chunk.SIZE;
            int localY = tileY - chunkY * Chunk.SIZE;

            // Validação extra (embora não seja mais necessária)
            if (localX < 0 || localX >= Chunk.SIZE || localY < 0 || localY >= Chunk.SIZE) {
                return false;
            }

            if (popupOpen && selectedX == tileX && selectedY == tileY) {
                popupOpen = false;
            } else {
                selectedX = tileX;
                selectedY = tileY;
                Chunk chunk = chunkManager.getChunk(chunkX, chunkY);
                selectedTile = chunk.getTile(localX, localY);
                popupOpen = true;
            }
        } catch (Exception e) {
            Gdx.app.error("GameScreen", "Erro ao processar clique no tile", e);
            game.setScreen(new BugCenterScreen(game, 
                "Erro ao clicar no tile:\n" + e.toString()));
            return false;
        }
        return false;
    }

    @Override
    public boolean longPress(float x, float y) {
        return false;
    }

    @Override
    public boolean fling(float velocityX, float velocityY, int button) {
        return false;
    }

    @Override
    public boolean pan(float x, float y, float deltaX, float deltaY) {
        if (!pauseMenuOpen && !settingsOpen) {
            try {
                float finalDeltaY = invertScrollY ? -deltaY : deltaY;
                panOffset.add(-deltaX * zoom * scrollSensitivity, 
                              finalDeltaY * zoom * scrollSensitivity);
            } catch (Exception e) {
                Gdx.app.error("GameScreen", "Erro no pan", e);
            }
        }
        return false;
    }
    @Override
    public boolean panStop(float x, float y, int pointer, int button) {
        return false;
    }

    @Override
    public boolean zoom(float initialDistance, float distance) {
        if (!pauseMenuOpen && !settingsOpen) {
            try {
                float delta = distance - initialDistance;
                if (invertPinch) delta = -delta;
                zoom += delta * pinchSensitivity;
                zoom = Math.max(0.5f, Math.min(3.0f, zoom));
            } catch (Exception e) {
                Gdx.app.error("GameScreen", "Erro no zoom", e);
            }
        }
        return false;
    }

    @Override
    public boolean pinch(Vector2 initialPointer1, Vector2 initialPointer2, Vector2 pointer1, Vector2 pointer2) {
        return false;
    }

    @Override
    public void pinchStop() {}

    @Override
    public void resize(int width, int height) {
        try {
            viewport.update(width, height, true);
        } catch (Exception e) {
            Gdx.app.error("GameScreen", "Erro no resize", e);
        }
    }

    @Override
    public void pause() {}
    @Override
    public void resume() {}
    @Override
    public void hide() {}

    @Override
    public void dispose() {
        try {
            if (whitePixel != null) whitePixel.dispose();
            if (tileTextures != null) {                for (Texture t : tileTextures) if (t != null) t.dispose();
            }
            if (batch != null) batch.dispose();
            if (font != null) font.dispose();
        } catch (Exception e) {
            Gdx.app.error("GameScreen", "Erro no dispose", e);
        }
    }
}