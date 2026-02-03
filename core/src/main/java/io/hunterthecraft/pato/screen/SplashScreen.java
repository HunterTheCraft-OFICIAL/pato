// core/src/io/hunterthecraft/pato/screen/SplashScreen.java
package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.utils.ScreenUtils;
import io.hunterthecraft.pato.PatoGame;
import io.hunterthecraft.pato.screen.ErrorScreen;
import io.hunterthecraft.pato.screen.MainMenuScreen;

public class SplashScreen implements Screen {
    private PatoGame game;
    private SpriteBatch batch;
    private Texture logo;

    public SplashScreen(PatoGame game) {
        this.game = game;
    }

    @Override
    public void show() {
        batch = game.batch;
        try {
            // Usa o logo gerado por você!
            logo = new Texture("fallback_assets/logo.png");
        } catch (Exception e) {
            Gdx.app.error("SplashScreen", "Falha ao carregar logo", e);
            logo = null;
        }

        // Agende transição com proteção total
        Gdx.app.postRunnable(() -> {
            try {
                game.setScreen(new MainMenuScreen(game));
            } catch (Exception e) {
                Gdx.app.error("SplashScreen", "Falha ao abrir menu", e);
                game.setScreen(new ErrorScreen(game, "Erro no menu:\n" + e.toString()));
            }
        });
    }

    @Override
    public void render(float delta) {
        ScreenUtils.clear(0.1f, 0.1f, 0.15f, 1);
        batch.begin();
        if (logo != null) {
            float x = (Gdx.graphics.getWidth() - logo.getWidth()) / 2f;
            float y = (Gdx.graphics.getHeight() - logo.getHeight()) / 2f;
            batch.draw(logo, x, y);
        }
        batch.end();
    }

    @Override
    public void dispose() {
        if (logo != null) logo.dispose();
    }

    @Override public void resize(int width, int height) {}
    @Override public void pause() {}
    @Override public void resume() {}
    @Override public void hide() {}
}