// core/src/io/hunterthecraft/pato/screen/BugCenterScreen.java
package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.scenes.scene2d.Stage;
import com.badlogic.gdx.scenes.scene2d.ui.TextButton;
import com.badlogic.gdx.scenes.scene2d.ui.Label;
import com.badlogic.gdx.scenes.scene2d.ui.Skin;
import com.badlogic.gdx.scenes.scene2d.ui.Table;
import com.badlogic.gdx.scenes.scene2d.utils.ClickListener;
import com.badlogic.gdx.utils.Clipboard;
import com.badlogic.gdx.utils.viewport.ScreenViewport;
import io.hunterthecraft.pato.PatoGame;

public class BugCenterScreen implements Screen {
    private PatoGame game;
    private Stage stage;
    private String fullLog;

    public BugCenterScreen(PatoGame game, String log) {
        this.game = game;
        this.fullLog = log != null ? log : "Sem logs disponíveis.";
    }

    @Override
    public void show() {
        stage = new Stage(new ScreenViewport());
        Gdx.input.setInputProcessor(stage);

        BitmapFont font = new BitmapFont();
        font.setColor(Color.WHITE);
        font.getData().setScale(1.0f);

        Skin skin = new Skin();
        TextButton.TextButtonStyle btnStyle = new TextButton.TextButtonStyle();
        btnStyle.font = font;
        btnStyle.fontColor = Color.BLACK;
        skin.add("default", btnStyle);

        Table table = new Table();
        table.setFillParent(true);
        table.left().pad(20);

        // Botões verticais
        TextButton menuBtn = new TextButton("Menu", skin);
        menuBtn.addListener(new ClickListener() {
            @Override            public void clicked(com.badlogic.gdx.scenes.scene2d.InputEvent event, float x, float y) {
                game.setScreen(new StartupScreen(game));
            }
        });
        table.add(menuBtn).width(140).height(50).row();

        TextButton copyBtn = new TextButton("Copiar", skin);
        copyBtn.addListener(new ClickListener() {
            @Override
            public void clicked(com.badlogic.gdx.scenes.scene2d.InputEvent event, float x, float y) {
                Clipboard clipboard = Gdx.app.getClipboard();
                clipboard.setContents(fullLog);
            }
        });
        table.add(copyBtn).width(140).height(50).row();

        TextButton exitBtn = new TextButton("Sair", skin);
        exitBtn.addListener(new ClickListener() {
            @Override
            public void clicked(com.badlogic.gdx.scenes.scene2d.InputEvent event, float x, float y) {
                Gdx.app.exit();
            }
        });
        table.add(exitBtn).width(140).height(50).row();

        // Área de logs
        Label logLabel = new Label(
            "Todos os logs gerados,\nmesmo que o relevante para\ntemos visão total",
            new Label.LabelStyle(font, Color.WHITE)
        );
        logLabel.setWrap(true);
        logLabel.setWidth(400);

        Table right = new Table();
        right.defaults().pad(10);
        right.add(logLabel).width(400).expandY().fillY();

        table.add(right).expand().fill();

        stage.addActor(table);
    }

    @Override
    public void render(float delta) {
        Gdx.gl.glClearColor(0, 0, 0, 1);
        Gdx.gl.glClear(com.badlogic.gdx.GL20.GL_COLOR_BUFFER_BIT);
        stage.act(delta);
        stage.draw();
    }
    @Override
    public void resize(int width, int height) {
        stage.getViewport().update(width, height, true);
    }

    @Override public void pause() {}
    @Override public void resume() {}
    @Override public void hide() {}
    @Override public void dispose() {
        if (stage != null) stage.dispose();
    }
}