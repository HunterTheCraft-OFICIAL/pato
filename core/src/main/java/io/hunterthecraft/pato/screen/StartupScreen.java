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

        // Atualiza progresso
        timer += delta;
        if (progress < 1.0f) {
            progress = Math.min(1.0f, timer / 2.0f); // 2 segundos para 100%
        }

        batch.begin();

        // Logo LibGDX (topo)
        font.setColor(Color.LIGHT_GRAY);
        layout.setText(font, "Logo LibGDX");
        font.draw(batch, layout, 20, Gdx.graphics.getBackBufferHeight() - 20);

        // Título "Pato"
        font.setColor(Color.WHITE);
        layout.setText(font, "Pato");
        float x = Gdx.graphics.getBackBufferWidth() / 2f - layout.width / 2f;
        float y = Gdx.graphics.getBackBufferHeight() / 2f + layout.height / 2f;
        font.draw(batch, layout, x, y);

        // Barra de progresso
        float barWidth = Gdx.graphics.getBackBufferWidth() - 80;
        float barX = 40;
        float barY = Gdx.graphics.getBackBufferHeight() / 2f - 40;
        // Fundo da barra
        drawRect(batch, barX, barY, barWidth, 16, Color.DARK_GRAY);
        // Progresso
        drawRect(batch, barX, barY, barWidth * progress, 16, Color.WHITE);

        // % texto
        font.setColor(Color.WHITE);
        String percent = String.format("%.0f%%", progress * 100);
        layout.setText(font, percent);
        font.draw(batch, layout, 
                  barX + barWidth / 2f - layout.width / 2f, 
                  barY - 20);

        batch.end();

        // Após 2s, vai para o menu
        if (timer >= 2.0f) {
            game.setScreen(new MainMenuScreen(game));
        }
    }

    // Desenha um retângulo sólido sem texturas
    private void drawRect(SpriteBatch batch, float x, float y, float width, float height, Color color) {
        if (width <= 0) return;
        batch.setColor(color);
        batch.draw(batch.getTexture(), x, y, width, height);
        batch.setColor(Color.WHITE);
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