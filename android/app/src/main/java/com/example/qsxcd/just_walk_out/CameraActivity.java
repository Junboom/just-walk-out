package com.example.qsxcd.just_walk_out;

import android.os.StrictMode;
import android.util.Log;

        import android.content.Intent;
        import android.graphics.Bitmap;
        import android.graphics.BitmapFactory;
        import android.graphics.Matrix;
        import android.graphics.PixelFormat;
        import android.hardware.Camera;
        import android.hardware.Camera.AutoFocusCallback;
        import android.hardware.Camera.PictureCallback;
        import android.hardware.Camera.ShutterCallback;
        import android.os.Bundle;
        import android.os.Environment;
        import android.support.v7.app.AppCompatActivity;
        import android.util.Log;
        import android.view.LayoutInflater;
        import android.view.SurfaceHolder;
        import android.view.SurfaceView;
        import android.view.View;
        import android.view.ViewGroup;
        import android.view.WindowManager;
        import android.widget.Button;
        import android.widget.LinearLayout;

import com.amazonaws.auth.CognitoCachingCredentialsProvider;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferObserver;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferUtility;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.rekognition.AmazonRekognitionClient;
import com.amazonaws.services.rekognition.model.FaceRecord;
import com.amazonaws.services.rekognition.model.Image;
import com.amazonaws.services.rekognition.model.IndexFacesRequest;
import com.amazonaws.services.rekognition.model.IndexFacesResult;
import com.amazonaws.services.rekognition.model.S3Object;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.regions.Region;
import com.amazonaws.regions.Regions;

import java.io.ByteArrayOutputStream;
        import java.io.File;
        import java.io.FileNotFoundException;
        import java.io.FileOutputStream;
        import java.io.IOException;
import java.util.List;

public class CameraActivity extends AppCompatActivity implements SurfaceHolder.Callback{

    Camera camera;
    SurfaceView surfaceView;
    SurfaceHolder surfaceHolder;
    boolean previewing = false;
    LayoutInflater controlInflater = null;

    timerThread timerthread;

    Button buttonTakePickture;

    Intent beforeIntent;
    Intent resultIntent;

    CognitoCachingCredentialsProvider credentialsProvider;
    AmazonS3 amazonS3;
    AmazonRekognitionClient amazonRekognition;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_camera);
        //setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);

        beforeIntent = getIntent();
        resultIntent = new Intent();
        resultIntent.putExtra("camera", "value");

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        init();


/*

        timerthread = new timerThread();
        timerthread.start();
        Log.e("쓰레드 시작", "ㅇ");
*/


    }


    public void init(){
        getWindow().setFormat(PixelFormat.UNKNOWN);
        surfaceView = (SurfaceView)findViewById(R.id.surfaceview_camera);
        surfaceHolder = surfaceView.getHolder();
        surfaceHolder.addCallback(this);
        surfaceHolder.setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);

        controlInflater = LayoutInflater.from(getBaseContext());
        View viewControl = controlInflater.inflate(R.layout.control, null);
        ViewGroup.LayoutParams layoutParamsControl = new ViewGroup.LayoutParams(ViewGroup.LayoutParams.FILL_PARENT, ViewGroup.LayoutParams.FILL_PARENT);
        this.addContentView(viewControl, layoutParamsControl);


        buttonTakePickture = (Button)findViewById(R.id.takepicture);


        buttonTakePickture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                camera.takePicture(myshutterCallback, myPictureCallback_RAW, myPictureCallback_JPG);

            }
        });


        LinearLayout layoutBackground = (LinearLayout)findViewById(R.id.background);
        layoutBackground.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                buttonTakePickture.setEnabled(false);
                camera.autoFocus(myAutoFocusCallback);
            }
        });


    }



    public void surfaceChanged(SurfaceHolder holder, int format, int width, int height){
        if(previewing){
            camera.stopPreview();
            previewing = false;
        }

        if(camera != null){
            try{
                camera.setPreviewDisplay(surfaceHolder);
                camera.startPreview();
                previewing = true;
            }catch (Exception e){
                e.printStackTrace();
            }
        }
    }

    public void surfaceCreated(SurfaceHolder holder){
        camera = Camera.open(1);        // 디폴트, 0은 후면 , 1은 전면
        camera.setDisplayOrientation(90); // 카메라 각도조정
    }

    public void surfaceDestroyed(SurfaceHolder holder){
        camera.stopPreview();
        camera.release();
        camera = null;
        previewing = false;
    }

    AutoFocusCallback myAutoFocusCallback = new AutoFocusCallback(){
        public void onAutoFocus(boolean arg0, Camera arg1){
            buttonTakePickture.setEnabled(true);
        }
    };


    // shutter Callback
    ShutterCallback myshutterCallback = new ShutterCallback() {
        @Override
        public void onShutter() {

        }
    };


    // Picture Callback
    PictureCallback myPictureCallback_RAW =  new PictureCallback() {
        @Override
        public void onPictureTaken(byte[] bytes, Camera camera) {

        }
    };

    // Picture Callback - 사진저장
    PictureCallback myPictureCallback_JPG = new PictureCallback() {

        @Override
        public void onPictureTaken(byte[] bytes, Camera camera) {

            //이미지의 너비와 높이 결정
            int w = camera.getParameters().getPictureSize().width;
            int h = camera.getParameters().getPictureSize().height;

            //byte array를 bitmap으로 변환
            BitmapFactory.Options options = new BitmapFactory.Options();
            options.inPreferredConfig = Bitmap.Config.ARGB_8888;
            Bitmap bitmap = BitmapFactory.decodeByteArray( bytes, 0, bytes.length, options);
            //int w = bitmap.getWidth();
            //int h = bitmap.getHeight();

            //이미지를 디바이스 방향으로 회전
            Matrix matrix = new Matrix();
            matrix.postRotate(270);
            bitmap =  Bitmap.createBitmap(bitmap, 0, 0, w, h, matrix, true);

            //bitmap을 byte array로 변환
            ByteArrayOutputStream stream = new ByteArrayOutputStream();
            bitmap.compress(Bitmap.CompressFormat.JPEG, 100, stream);
            byte[] currentData = stream.toByteArray();


            try{

                FileOutputStream imageFileOs;


                // 새로만들어서 넣을 파일 위치를 임의의 외부 스토리지(디렉터리)에 만듦
               /* File sdCard = Environment.getExternalStorageDirectory();
                File dir = new File(sdCard.getAbsolutePath() + "/HansungPass");
                */

                // 새로만들어서 넣을 파일 위치를 내부 스토리지로 설정
                File dir = getExternalFilesDir(Environment.DIRECTORY_PICTURES);

                dir.mkdirs();

                // 사진이름 설정
                String fileName = String.format("%d.jpg", "FaceID");
                File outFile = new File(dir, fileName);
                Log.e("경로: ", outFile.getAbsolutePath());
                imageFileOs = new FileOutputStream(outFile);
                imageFileOs.write(currentData);
                imageFileOs.flush();
                imageFileOs.close();        // 파일 저장 끝


                File s3_file = s3();

                /*try {
                    Thread.sleep(1000);
                }catch (Exception e){
                    }*/

                String id_value = getId(s3_file);

                resultIntent.putExtra("id", id_value);       // 회원가입activity로 값을 넘겨주는 부분
                setResult(RESULT_OK, resultIntent);

                finish(); // 현재 카메라 액티비티 종료


            }catch (FileNotFoundException e){
                e.printStackTrace();
            }catch(IOException e){
                e.printStackTrace();
            }




        }
    };


    public File s3(){
        System.out.println("s3내부");

        credentialsProvider = new CognitoCachingCredentialsProvider( //코그니토 자격증명하면 이 코드 그대로 줌
                getApplicationContext(),
                "ap-northeast-1:efee39c0-819c-46ea-8d61-68f273b7645c", // 자격 증명 풀 ID
                Regions.AP_NORTHEAST_1 // 리전
        );

        amazonS3 = new AmazonS3Client(credentialsProvider);
        //amazonS3.setRegion(Region.getRegion(Regions.AP_NORTHEAST_1));
        amazonS3.setRegion(Region.getRegion(Regions.AP_NORTHEAST_1));
        amazonS3.setEndpoint("s3.ap-northeast-1.amazonaws.com");

        System.out.println("s3내부2");

        File file = new File("/storage/emulated/0/Android/data/com.example.qsxcd.just_walk_out/files/Pictures/1111.jpg");

        if (amazonS3 != null) {

            if(file.exists()) {
                System.out.println("s3내부3");

                TransferUtility transferUtility = new TransferUtility(amazonS3, getApplicationContext());
                System.out.println("s3내부4: "+file.getName());
                TransferObserver observer = transferUtility.upload(
                        "chanmo",
                        file.getName(),
                        file
                );

                System.out.println("파일이름:" + file.getName());
            }
        }

        return file;

    }

    public String getId(File file){

        amazonRekognition = new AmazonRekognitionClient(credentialsProvider); //레코그니션 자격증명에 파라미터로 코그니토
        amazonRekognition.setEndpoint("rekognition.ap-northeast-1.amazonaws.com");
        amazonRekognition.setRegion(Region.getRegion(Regions.AP_NORTHEAST_1));


        //Image image = new Image().withS3Object(new S3Object().withBucket("chanmo").withName(file.getName())); // 이미지 호출
        Image image = new Image().withS3Object(new S3Object().withBucket("chanmo").withName(file.getName()));

        IndexFacesRequest indexFacesRequest = new IndexFacesRequest().withImage(image).withCollectionId("RekognitionCollection")
                .withExternalImageId(file.getName()).withDetectionAttributes("ALL"); //이미지 분석 리퀘스트

        IndexFacesResult indexFacesResult = amazonRekognition.indexFaces(indexFacesRequest); // 결과

        List<FaceRecord> faceRecords = indexFacesResult.getFaceRecords(); // 결과 출력
        String return_id="";

        for (FaceRecord faceRecord : faceRecords) {
            System.out.println("Face detected: Faceid is " + faceRecord.getFace().getFaceId());
            return_id = faceRecord.getFace().getFaceId();
        }

        return return_id;
    }







    class timerThread extends Thread{

        timerThread(){
            Log.e("쓰레드 만들어짐", "ㅇ");
        }

        @Override
        public void run(){
            Log.e("run들어옴", "ㅇ");
            while(true) {

                Log.e("사진찍음 : ", "try전");
                try {
                    Thread.sleep(500);
                    // shutter 부분을 null 처리하면 소리가 안난다.
                    //camera.takePicture(myshutterCallback, myPictureCallback_RAW, myPictureCallback_JPG);
                    camera.takePicture(myshutterCallback, myPictureCallback_RAW, myPictureCallback_JPG);
                    Log.e("사진찍음 : ", "try후");
                } catch (Exception e) {

                }
            }
        }


    }
}
