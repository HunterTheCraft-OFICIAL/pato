// core/src/io/hunterthecraft/pato/screen/StartupScreen.java
package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.graphics.g2d.GlyphLayout;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.utils.ScreenUtils;
import io.hunterthecraft.pato.PatoGame;

public class StartupScreen implements Screen {
    private PatoGame game;
    private SpriteBatch batch;
    private BitmapFont font;
    private GlyphLayout layout;
    private float progress = 0f;
    private float timer = 0f;

    public StartupScreen(PatoGame game) {
        this.game = game;
    }

    @Override
    public void show() {
        batch = new SpriteBatch();
        font = new BitmapFont();
        font.getData().setScale(2.5f);
        layout = new GlyphLayout();
    }

    @Override
    public void render(float delta) {
        ScreenUtils.clear(0, 0, 0.2f, 1);

        timer += delta;
        if (progress < 1.0f) {
            progress = Math.min(1.0f, timer / 2.0f);
        }

        batch.begin();

        // Logo LibGDX
        font.setColor(Color.LIGHT_GRAY);
        layout.setText(font, "Logo LibGDX");
        font.draw(batch, layout, 20, Gdx.graphics.getBackBufferHeight() - 20);

        // Título "Pato"
        font.setColor(Color.WHITE);
        layout.setText(font, "Pato");
        float x = Gdx.graphics.getBackBufferWidth() / 2f - layout.width / 2f;
        float y = Gdx.graphics.getBackBufferHeight() / 2f + layout.height / 2f;
        font.draw(batch, layout, x, y);

        // Progresso como texto (sem barra gráfica)
        font.setColor(Color.GREEN);
        String status = String.format("Carregando... %.0f%%", progress * 100);
        layout.setText(font, status);
        float px = Gdx.graphics.getBackBufferWidth() / 2f - layout.width / 2f;
        float py = Gdx.graphics.getBackBufferHeight() / 2f - 50;
        font.draw(batch, layout, px, py);

        batch.end();

        if (timer >= 2.0f) {
            game.setScreen(new MainMenuScreen(game));
        }
    }

    @Override public void resize(int width, int height) {}
    @Override public void pause() {}
    @Override public void resume() {}
    @Override public void hide() {}
    @Override public void dispose() {
        if (batch != null) batch.dispose();
        if (font != null) font.dispose();
    }
}