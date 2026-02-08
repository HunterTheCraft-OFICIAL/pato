// core/src/io/hunterthecraft/pato/screen/GameScreen.java
package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.GL20;
import com.badlogic.gdx.graphics.OrthographicCamera;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.graphics.g2d.GlyphLayout;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.math.Vector2;
import com.badlogic.gdx.utils.ScreenUtils;
import com.badlogic.gdx.utils.viewport.ScreenViewport;
import io.hunterthecraft.pato.PatoGame;
import io.hunterthecraft.pato.data.TileType;
import io.hunterthecraft.pato.model.WorldData;

public class GameScreen implements Screen {
    private PatoGame game;
    private SpriteBatch batch;
    private BitmapFont font;
    private GlyphLayout layout;
    private WorldData world;
    private Texture[] tileTextures;

    // Câmera e interação
    private OrthographicCamera camera;
    private ScreenViewport viewport;
    private float zoom = 1.0f;
    private boolean isDragging = false;
    private Vector2 dragStart = new Vector2();
    private Vector2 lastTouch = new Vector2();

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
        font.getData().setScale(1.0f);        layout = new GlyphLayout();

        // Câmera
        camera = new OrthographicCamera();
        viewport = new ScreenViewport(camera);
        viewport.update(Gdx.graphics.getWidth(), Gdx.graphics.getHeight(), true);

        // Carrega texturas
        tileTextures = new Texture[2];
        tileTextures[0] = new Texture(world.biomeA.getAssetPath());
        tileTextures[1] = new Texture(world.biomeB.getAssetPath());
    }

    @Override
    public void render(float delta) {
        // Atualiza câmera
        camera.position.set(0, 0, 0);
        camera.zoom = 1.0f / zoom;
        camera.update();
        batch.setProjectionMatrix(camera.combined);

        // Fundo
        ScreenUtils.clear(0.1f, 0.1f, 0.15f, 1);

        // Processamento de input
        handleInput();

        // Renderização
        batch.begin();

        int tileSize = 128;
        float offsetX = -world.width * tileSize / 2f;
        float offsetY = -world.height * tileSize / 2f;

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

            // Fundo da pop-up (retângulo branco semi-transparente)
            drawRect(batch, px, py, 200, 100, new Color(0, 0, 0, 0.7f));
            // Texto
            font.setColor(Color.WHITE);
            layout.setText(font, "Bioma: " + selectedTile.name);
            font.draw(batch, layout, px + 10, py + 80);

            layout.setText(font, String.format("Coord: (%d, %d)", selectedX, selectedY));
            font.draw(batch, layout, px + 10, py + 60);

            // Botão X
            layout.setText(font, "✕");
            font.draw(batch, layout, px + 180, py + 90);
        }

        batch.end();
    }

    private void handleInput() {
        // Zoom (simulado com tecla de volume ou botão virtual no futuro)
        // Por enquanto, use dois dedos ou mantenha simples
        if (Gdx.input.isTouched()) {
            if (!isDragging) {
                isDragging = true;
                dragStart.set(Gdx.input.getX(), Gdx.input.getY());
                lastTouch.set(dragStart);
            } else {
                float dx = Gdx.input.getX() - lastTouch.x;
                float dy = Gdx.input.getY() - lastTouch.y;
                camera.translate(-dx * zoom, dy * zoom); // inverte Y
                lastTouch.set(Gdx.input.getX(), Gdx.input.getY());
            }
        } else {
            isDragging = false;
        }

        // Zoom com roda do mouse (desktop) ou botões (mobile futuramente)
        if (Gdx.input.getDeltaWheel() != 0) {
            zoom += Gdx.input.getDeltaWheel() * 0.1f;
            zoom = Math.max(0.5f, Math.min(3.0f, zoom));
        }

        // Clique em tile
        if (Gdx.input.justTouched() && !isDragging) {
            float touchX = Gdx.input.getX();
            float touchY = Gdx.input.getY();

            // Converte para coordenadas do mundo
            Vector2 worldPos = viewport.unproject(new Vector2(touchX, touchY));
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

            // Verifica clique no botão X
            if (popupOpen) {
                float px = offsetX + selectedX * tileSize;
                float py = offsetY + selectedY * tileSize + tileSize;
                if (touchX > px + 180 && touchX < px + 200 &&
                    touchY > py + 80 && touchY < py + 100) {
                    popupOpen = false;
                }
            }
        }
    }

    // Desenha um retângulo sólido sem textura
    private void drawRect(SpriteBatch batch, float x, float y, float width, float height, Color color) {
        Gdx.gl.glEnable(GL20.GL_BLEND);
        Gdx.gl.glBlendFunc(GL20.GL_SRC_ALPHA, GL20.GL_ONE_MINUS_SRC_ALPHA);
        batch.setColor(color);
        batch.draw(batch.getTexture(), x, y, width, height);
        batch.setColor(Color.WHITE);
        Gdx.gl.glDisable(GL20.GL_BLEND);
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
        if (tileTextures != null) {
            for (Texture tex : tileTextures) {
                if (tex != null) tex.dispose();
            }
        }
        if (batch != null) batch.dispose();        if (font != null) font.dispose();
    }
}