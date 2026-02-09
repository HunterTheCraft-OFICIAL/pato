// core/src/io/hunterthecraft/pato/screen/WorldLoadingScreen.java
package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.utils.ScreenUtils;
import io.hunterthecraft.pato.PatoGame;

public class WorldLoadingScreen implements Screen {
    private PatoGame game;

    public WorldLoadingScreen(PatoGame game) {
        this.game = game;
    }

    @Override
    public void show() {
        // Carrega assets em background
        Gdx.app.postRunnable(() -> {
            try {
                // Testa se os assets essenciais existem
                Texture amazonia = new Texture("tiles/debug_amazonia.png");
                Texture cerrado = new Texture("tiles/debug_cerrado.png");
                
                // Libera as texturas (só testamos a existência)
                amazonia.dispose();
                cerrado.dispose();

                // Vai para o mundo infinito
                game.setScreen(new GameScreen(game));
            } catch (Exception e) {
                Gdx.app.error("WorldLoading", "Falha ao carregar assets", e);
                game.setScreen(new BugCenterScreen(game, 
                    "Erro ao carregar assets:\n" + e.getMessage()));
            }
        });
    }

    @Override
    public void render(float delta) {
        // Tela de carregamento simples
        ScreenUtils.clear(0.1f, 0.1f, 0.2f, 1);
        
        // Opcional: adicionar texto "Carregando mundo..." depois
    }

    @Override public void resize(int width, int height) {}
    @Override public void pause() {}
    @Override public void resume() {}
    @Override public void hide() {}
    @Override public void dispose() {}
}