// core/src/io/hunterthecraft/pato/screen/ErrorScreen.java
package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.utils.ScreenUtils;
import com.badlogic.gdx.scenes.scene2d.Stage;
import com.badlogic.gdx.scenes.scene2d.ui.TextButton;
import com.badlogic.gdx.scenes.scene2d.ui.Label;
import com.badlogic.gdx.scenes.scene2d.ui.Skin;
import com.badlogic.gdx.scenes.scene2d.ui.Table;
import com.badlogic.gdx.scenes.scene2d.utils.ClickListener;
import com.badlogic.gdx.utils.viewport.ScreenViewport;
import com.badlogic.gdx.utils.Clipboard;
import io.hunterthecraft.pato.PatoGame;

public class ErrorScreen implements Screen {
    private PatoGame game;
    private Stage stage;
    private String errorMessage;

    public ErrorScreen(PatoGame game, String errorMessage) {
        this.game = game;
        this.errorMessage = errorMessage != null ? errorMessage : "Erro desconhecido";
    }

    @Override
    public void show() {
        stage = new Stage(new ScreenViewport());
        Gdx.input.setInputProcessor(stage);

        BitmapFont font = new BitmapFont(Gdx.files.internal("ui/font.fnt"));
        font.getData().setScale(0.8f);

        Skin skin = new Skin();
        TextButton.TextButtonStyle buttonStyle = new TextButton.TextButtonStyle();
        buttonStyle.font = font;
        buttonStyle.fontColor = Color.WHITE;
        skin.add("default", buttonStyle);

        Label.LabelStyle labelStyle = new Label.LabelStyle(font, Color.RED);
        Label errorLabel = new Label("Erro Crítico:\n" + errorMessage, labelStyle);
        errorLabel.setWrap(true);
        errorLabel.setWidth(350);

        Table table = new Table();
        table.setFillParent(true);
        table.center().top().padTop(50);        table.add(errorLabel).width(350).padBottom(30).row();

        // Copiar Logs
        TextButton copyButton = new TextButton("Copiar Logs", skin);
        copyButton.addListener(new ClickListener() {
            @Override
            public void clicked(com.badlogic.gdx.scenes.scene2d.InputEvent event, float x, float y) {
                Clipboard clipboard = Gdx.app.getClipboard();
                clipboard.setContents(errorMessage);
            }
        });
        table.add(copyButton).width(200).height(40).padBottom(10).row();

        // Menu Principal
        TextButton menuButton = new TextButton("Menu Principal", skin);
        menuButton.addListener(new ClickListener() {
            @Override
            public void clicked(com.badlogic.gdx.scenes.scene2d.InputEvent event, float x, float y) {
                game.setScreen(new SplashScreen(game));
            }
        });
        table.add(menuButton).width(200).height(40).padBottom(10).row();

        // Sair
        TextButton exitButton = new TextButton("Sair", skin);
        exitButton.addListener(new ClickListener() {
            @Override
            public void clicked(com.badlogic.gdx.scenes.scene2d.InputEvent event, float x, float y) {
                Gdx.app.exit();
            }
        });
        table.add(exitButton).width(200).height(40).row();

        stage.addActor(table);
    }

    @Override
    public void render(float delta) {
        ScreenUtils.clear(0.2f, 0.0f, 0.0f, 1); // vermelho escuro
        stage.act(delta);
        stage.draw();
    }

    @Override
    public void resize(int width, int height) {
        stage.getViewport().update(width, height, true);
    }

    @Override public void pause() {}
    @Override public void resume() {}    @Override public void hide() {}
    @Override
    public void dispose() {
        if (stage != null) stage.dispose();
    }
}