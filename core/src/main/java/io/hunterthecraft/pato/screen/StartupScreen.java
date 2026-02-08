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
        font = new BitmapFont(); // usa fonte embutida
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
        layout.setText(font, "Logo LibGDX");
        font.draw(batch, layout, 20, Gdx.graphics.getHeight() - 20);

        // Título "Pato"
        font.setColor(Color.WHITE);
        layout.setText(font, "Pato");
        float x = (Gdx.graphics.getWidth() - layout.width) / 2;
        float y = Gdx.graphics.getHeight() / 2 + layout.height / 2;
        font.draw(batch, layout, x, y);

        // Simples texto de progresso (sem barra gráfica por enquanto)
        font.setColor(Color.GREEN);
        layout.setText(font, String.format("Carregando... %.0f%%", progress * 100));
        font.draw(batch, layout, 
                  (Gdx.graphics.getWidth() - layout.width) / 2, 
                  Gdx.graphics.getHeight() / 2 - 50);

        batch.end();

        // Simula carregamento
        if (!loadingDone) {
            progress += delta * 0.2f;
            if (progress >= 1.0f) {
                progress = 1.0f;
                loadingDone = true;
                // Por enquanto, não vai para MainMenuScreen (ainda não existe)
                // Em breve, você adicionará essa transição
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