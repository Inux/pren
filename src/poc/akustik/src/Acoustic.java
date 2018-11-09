import com.sun.speech.freetts.FreeTTS;
import javafx.application.Application;
import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;
import javafx.stage.Stage;


import java.io.File;

import static java.lang.Thread.sleep;

public class Acoustic extends Application{

    public void playSoundByNumber(int number) throws InterruptedException {

        //com.sun.javafx.application.PlatformImpl.startup(()->{});
        Application.launch();
        String bip = System.getProperty("user.dir") + "/Soundfiles/E9.wav";

        File soundFile = new File(bip);
        Media hit = new Media(soundFile.toURI().toString());
        MediaPlayer mediaPlayer = new MediaPlayer(hit);
        mediaPlayer.play();

        //sleep(1000);
    }

    public static void playTextByNumber(int number){

    }

    @Override
    public void start(Stage primaryStage) throws Exception {
        String bip = System.getProperty("user.dir") + "/Soundfiles/E9.wav";
        System.out.println(bip);
        File soundFile = new File(bip);
        Media hit = new Media(soundFile.toURI().toString());
        MediaPlayer mediaPlayer = new MediaPlayer(hit);
        mediaPlayer.play();
    }
}
