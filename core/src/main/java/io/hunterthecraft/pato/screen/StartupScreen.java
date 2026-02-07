// core/src/io/hunterthecraft/pato/screen/StartupScreen.java
package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.graphics.g2d.GlyphLayout;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.utils.ScreenUtils;
import com.badlogic.gdx.utils.viewport.FitViewport;
import io.hunterthecraft.pato.PatoGame;

public class StartupScreen implements Screen {
    private PatoGame game;
    private SpriteBatch batch;
    private FitViewport viewport;
    private BitmapFont font;
    private GlyphLayout layout;
    private float progress = 0f;
    private boolean loadingDone = false;

    public StartupScreen(PatoGame game) {
        this.game = game;
    }

    @Override
    public void show() {
        batch = new SpriteBatch();
        viewport = new FitViewport(800, 480);
        font = new BitmapFont();
        font.setColor(Color.WHITE);
        font.getData().setScale(3.0f);
        layout = new GlyphLayout();
    }

    @Override
    public void render(float delta) {
        ScreenUtils.clear(0, 0, 0, 1); // fundo preto

        viewport.apply();
        batch.setProjectionMatrix(viewport.getCamera().combined);
        batch.begin();

        // Logo LibGDX (topo)
        font.setColor(Color.LIGHT_GRAY);
        font.draw(batch, "Logo LibGDX", 20, viewport.getWorldHeight() - 20);

        // Título "Pato"
        font.setColor(Color.WHITE);
        layout.setText(font, "Pato");
        float x = (viewport.getWorldWidth() - layout.width) / 2;
        float y = viewport.getWorldHeight() / 2 + layout.height / 2;
        font.draw(batch, "Pato", x, y);

        // Barra de progresso
        float barWidth = viewport.getWorldWidth() - 80;
        float barX = 40;
        float barY = viewport.getWorldHeight() / 2 - 40;
        batch.setColor(Color.GRAY);
        batch.draw(batch.getTexture(), barX, barY, barWidth, 16);
        batch.setColor(Color.WHITE);
        batch.draw(batch.getTexture(), barX, barY, barWidth * progress, 16);

        // % texto
        font.setColor(Color.WHITE);
        font.draw(batch, String.format("%.0f%%", progress * 100), 
                  barX + barWidth / 2 - font.getBounds("00%").width / 2, barY - 25);

        batch.end();

        // Simula carregamento (substitua por AssetManager depois)
        if (!loadingDone) {
            progress += delta * 0.2f;
            if (progress >= 1.0f) {
                progress = 1.0f;
                loadingDone = true;
                // Aqui você troca para MainMenuScreen
                Gdx.app.postRunnable(() -> game.setScreen(new MainMenuScreen(game)));
            }
        }
    }

    @Override
    public void resize(int width, int height) {
        viewport.update(width, height, true);
    }

    @Override public void pause() {}
    @Override public void resume() {}
    @Override public void hide() {}
    @Override public void dispose() {
        if (batch != null) batch.dispose();
        if (font != null) font.dispose();
    }
}