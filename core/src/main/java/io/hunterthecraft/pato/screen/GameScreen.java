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

    public GameScreen(PatoGame game) {
        this.game = game;
    }

    @Override
    public void show() {        batch = new SpriteBatch();
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
    }

    @Override
    public void render(float delta) {
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
    }

    private void renderChunks() {
        int centerChunkX = (int) (camera.position.x / (Chunk.SIZE * TILE_SIZE));
        int centerChunkY = (int) (camera.position.y / (Chunk.SIZE * TILE_SIZE));

        int radius = 2;
        for (int cy = centerChunkY - radius; cy <= centerChunkY + radius; cy++) {
            for (int cx = centerChunkX - radius; cx <= centerChunkX + radius; cx++) {
                Chunk chunk = chunkManager.getChunk(cx, cy);
                for (int y = 0; y < Chunk.SIZE; y++) {
                    for (int x = 0; x < Chunk.SIZE; x++) {
                        TileType tile = chunk.getTile(x, y);
                        int globalX = cx * Chunk.SIZE + x;
                        int globalY = cy * Chunk.SIZE + y;
                        Texture tex = (tile == TileType.AMAZONIA) ? tileTextures[0] : tileTextures[1];
                        batch.draw(tex, globalX * TILE_SIZE, globalY * TILE_SIZE, TILE_SIZE, TILE_SIZE);
                    }
                }
            }
        }

        chunkManager.unloadDistantChunks(centerChunkX, centerChunkY);
    }

    private void drawPauseButton() {
        float btnX = Gdx.graphics.getWidth() - 60;
        float btnY = Gdx.graphics.getHeight() - 60;
        batch.setColor(0.2f, 0.2f, 0.3f, 0.8f);
        batch.draw(whitePixel, btnX, btnY, 50, 50);
        batch.setColor(1, 1, 1, 1);
        font.setColor(Color.WHITE);
        layout.setText(font, "⏸");
        font.draw(batch, layout, btnX + 15, btnY + 35);
    }

    private void drawPauseMenu() {        batch.setColor(0, 0, 0, 0.6f);
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

        layout.setText(font, "Sair");
        font.draw(batch, layout, 100, Gdx.graphics.getHeight() - 240);

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
    }

    private void drawSettingsMenu() {
        batch.setColor(0, 0, 0, 0.7f);
        batch.draw(whitePixel, 50, 50, Gdx.graphics.getWidth() - 100, Gdx.graphics.getHeight() - 100);
        batch.setColor(1, 1, 1, 1);

        font.setColor(Color.YELLOW);
        layout.setText(font, "CONFIGURAÇÕES");
        font.draw(batch, layout, 100, Gdx.graphics.getHeight() - 100);

        font.setColor(Color.WHITE);
        layout.setText(font, "Zoom Sensitivity: 0.005");
        font.draw(batch, layout, 100, Gdx.graphics.getHeight() - 150);

        layout.setText(font, "Render Distance: 2 chunks");
        font.draw(batch, layout, 100, Gdx.graphics.getHeight() - 190);
        layout.setText(font, "Voltar");
        font.draw(batch, layout, 100, 100);

        if (Gdx.input.justTouched() && Gdx.input.getY() < 150) {
            settingsOpen = false;
        }
    }

    @Override
    public boolean touchDown(float x, float y, int pointer, int button) {
        return false;
    }

    @Override
    public boolean tap(float x, float y, int count, int button) {
        if (pauseMenuOpen || settingsOpen) return false;

        Vector2 screenPos = new Vector2(x, y);
        Vector2 worldPos = viewport.unproject(screenPos);

        int tileX = (int) (worldPos.x / TILE_SIZE);
        int tileY = (int) (worldPos.y / TILE_SIZE);

        if (popupOpen && selectedX == tileX && selectedY == tileY) {
            popupOpen = false;
        } else {
            selectedX = tileX;
            selectedY = tileY;
            int chunkX = tileX / Chunk.SIZE;
            int chunkY = tileY / Chunk.SIZE;
            Chunk chunk = chunkManager.getChunk(chunkX, chunkY);
            selectedTile = chunk.getTile(tileX % Chunk.SIZE, tileY % Chunk.SIZE);
            popupOpen = true;
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
    public boolean pan(float x, float y, float deltaX, float deltaY) {        if (!pauseMenuOpen && !settingsOpen) {
            panOffset.add(-deltaX * zoom, deltaY * zoom);
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
            float delta = distance - initialDistance;
            zoom += delta * 0.005f;
            zoom = Math.max(0.5f, Math.min(3.0f, zoom));
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
        if (whitePixel != null) whitePixel.dispose();
        if (tileTextures != null) {
            for (Texture t : tileTextures) if (t != null) t.dispose();
        }
        if (batch != null) batch.dispose();        if (font != null) font.dispose();
    }
}