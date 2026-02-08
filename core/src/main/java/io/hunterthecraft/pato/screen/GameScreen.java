// core/src/io/hunterthecraft/pato/screen/GameScreen.java
package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.Color;
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
import io.hunterthecraft.pato.model.WorldData;

public class GameScreen implements Screen, GestureDetector.GestureListener {
    private PatoGame game;
    private SpriteBatch batch;
    private BitmapFont font;
    private GlyphLayout layout;
    private WorldData world;
    private Texture[] tileTextures;
    private Texture whitePixel; // ← usado para desenhar retângulos

    // Câmera
    private ScreenViewport viewport;
    private float zoom = 1.0f;
    private Vector2 panOffset = new Vector2();

    // Pop-up
    private TileType selectedTile = null;
    private int selectedX = -1, selectedY = -1;
    private boolean popupOpen = false;

    public GameScreen(PatoGame game, WorldData world) {
        this.game = game;
        this.world = world;
    }

    @Override
    public void show() {
        batch = new SpriteBatch();
        font = new BitmapFont();
        font.getData().setScale(1.0f);
        layout = new GlyphLayout();
        // Cria textura branca 1x1 para desenhar formas
        Pixmap pixmap = new Pixmap(1, 1, Pixmap.Format.RGBA8888);
        pixmap.setColor(Color.WHITE);
        pixmap.fill();
        whitePixel = new Texture(pixmap);
        pixmap.dispose();

        viewport = new ScreenViewport();
        viewport.update(Gdx.graphics.getWidth(), Gdx.graphics.getHeight(), true);

        // Carrega texturas dos biomas
        tileTextures = new Texture[2];
        tileTextures[0] = new Texture(world.biomeA.getAssetPath());
        tileTextures[1] = new Texture(world.biomeB.getAssetPath());

        // Configura input
        GestureDetector detector = new GestureDetector(this);
        Gdx.input.setInputProcessor(detector);
    }

    @Override
    public void render(float delta) {
        // Atualiza câmera
        viewport.getCamera().position.set(panOffset.x, panOffset.y, 0);
        viewport.getCamera().zoom = 1.0f / zoom;
        viewport.getCamera().update();
        batch.setProjectionMatrix(viewport.getCamera().combined);

        ScreenUtils.clear(0.1f, 0.1f, 0.15f, 1);
        batch.begin();

        int tileSize = 128;
        float offsetX = -world.width * tileSize / 2f;
        float offsetY = -world.height * tileSize / 2f;

        // Renderiza grid
        for (int y = 0; y < world.height; y++) {
            for (int x = 0; x < world.width; x++) {
                TileType tile = world.getTileAt(x, y);
                Texture tex = (tile == world.biomeA) ? tileTextures[0] : tileTextures[1];
                batch.draw(tex, offsetX + x * tileSize, offsetY + y * tileSize, tileSize, tileSize);
            }
        }

        // Pop-up
        if (popupOpen && selectedTile != null) {
            float px = offsetX + selectedX * tileSize;
            float py = offsetY + selectedY * tileSize + tileSize;

            // Fundo da pop-up            batch.setColor(0, 0, 0, 0.7f);
            batch.draw(whitePixel, px, py, 200, 100);
            batch.setColor(1, 1, 1, 1);

            // Texto
            font.setColor(Color.WHITE);
            layout.setText(font, "Bioma: " + selectedTile.toString()); // ← corrigido
            font.draw(batch, layout, px + 10, py + 80);

            layout.setText(font, String.format("Coord: (%d, %d)", selectedX, selectedY));
            font.draw(batch, layout, px + 10, py + 60);

            // Botão X
            layout.setText(font, "✕");
            font.draw(batch, layout, px + 180, py + 90);
        }

        batch.end();
    }

    // --- GestureDetector callbacks ---
    @Override
    public boolean touchDown(float x, float y, int pointer, int button) {
        return false;
    }

    @Override
    public boolean tap(float x, float y, int count, int button) {
        Vector2 worldPos = viewport.unproject(new Vector2(x, y));
        int tileSize = 128;
        float offsetX = -world.width * tileSize / 2f;
        float offsetY = -world.height * tileSize / 2f;

        int tileX = (int) ((worldPos.x - offsetX) / tileSize);
        int tileY = (int) ((worldPos.y - offsetY) / tileSize);

        if (tileX >= 0 && tileX < world.width && tileY >= 0 && tileY < world.height) {
            selectedX = tileX;
            selectedY = tileY;
            selectedTile = world.getTileAt(tileX, tileY);
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
    public boolean pan(float x, float y, float deltaX, float deltaY) {
        panOffset.add(-deltaX * zoom, deltaY * zoom); // inverte Y
        return false;
    }

    @Override
    public boolean zoom(float initialDistance, float distance) {
        float factor = distance / initialDistance;
        zoom *= factor;
        zoom = Math.max(0.5f, Math.min(3.0f, zoom));
        return false;
    }

    @Override
    public boolean pinch(Vector2 initialPointer1, Vector2 initialPointer2, Vector2 pointer1, Vector2 pointer2) {
        return false;
    }

    @Override
    public void pinchStop() {
        // Método obrigatório do GestureListener
    }

    @Override
    public void resize(int width, int height) {
        viewport.update(width, height, true);
    }

    @Override public void pause() {}
    @Override public void resume() {}
    @Override public void hide() {}

    @Override
    public void dispose() {
        if (whitePixel != null) whitePixel.dispose();
        if (tileTextures != null) {
            for (Texture t : tileTextures) if (t != null) t.dispose();
        }
        if (batch != null) batch.dispose();
        if (font != null) font.dispose();
    }
}