#include<bits/stdc++.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/core/utility.hpp>
#include <opencv2/video/video.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/videoio/videoio.hpp>
#include <opencv2/videostab/videostab.hpp>
#include <opencv2/opencv_modules.hpp>
#include <opencv2/imgcodecs.hpp>

using namespace std;
using namespace cv;

void getImage()
{
	string fname;
	int size;
	cout<<"Enter the image name:- \n";
	cin>>fname;
	Mat med_th;
	Mat img=imread(fname,1);
	cvtColor(img,med_th,COLOR_BGR2GRAY);
	Mat th;
	SimpleBlobDetector detector;
	//<<"Enter the size of blur\n";
	//cin>>size;

	//bilateralFilter ( med_th, med_th, size, size*2, size/2 );
	cout<<"Enter the size of blur\n";
	cin>>size;
	GaussianBlur( med_th, med_th, Size(size, size), 0, 0 );
	th=med_th;
	threshold(med_th, th, 0, 255, THRESH_BINARY | THRESH_OTSU);
	Canny(th, th, 51, 151, 3);
	int count=0;
    int max=-1;

    Point maxPt;

    for(int y=0;y<th.size().height;y++)
    {
        uchar *row = th.ptr(y);
        for(int x=0;x<th.size().width;x++)
        {
            if(row[x]>=128)
            {

                 int area = floodFill(th, Point(x,y), RGB(0,0,64));

                 if(area>max)
                 {
                     maxPt = Point(x,y);
                     max = area;
                 }
            }
        }

    }
	floodFill(th, maxPt, RBG(255,255,255));
	for(int y=0;y<th.size().height;y++)
    {
        uchar *row = th.ptr(y);
        for(int x=0;x<th.size().width;x++)
        {
            if(row[x]==64 && x!=maxPt.x && y!=maxPt.y)
            {
                int area = floodFill(th, Point(x,y), RGB(0,255,0));
            }
        }
    }
	Mat kernel = (Mat_<uchar>(3,3) << 0,1,0,1,1,1,0,1,0);
	erode(th, th, kernel);
    imshow("source", th);

	//GaussianBlur( med_th, med_th, Size(size, size), 0, 0 );
	//Mat element = getStructuringElement( MORPH_RECT,Size( 2*size + 1, 2*size+1 ),Point( size, size ) );
	 vector<Vec2f> lines;
	//std::vector<KeyPoint> keypoints;
	//detector.detect( th, keypoints);
	//Mat im_with_keypoints;
	//drawKeypoints( th, keypoints, im_with_keypoints, Scalar(0,0,255), DrawMatchesFlags::DRAW_RICH_KEYPOINTS );
	  //dilate( th, th, element );
		namedWindow("source",WINDOW_NORMAL); 
    HoughLines(th, lines, 1, CV_PI/180, 150, 0, 0 );
 	//imshow("source", im_with_keypoints );
    // draw lines
    for( size_t i = 0; i < lines.size(); i++ )
    {
        float rho = lines[i][0], theta = lines[i][1];
        Point pt1, pt2;
        double a = cos(theta), b = sin(theta);
        double x0 = a*rho, y0 = b*rho;
        pt1.x = cvRound(x0 + 1000*(-b));
        pt1.y = cvRound(y0 + 1000*(a));
        pt2.x = cvRound(x0 - 1000*(-b));
        pt2.y = cvRound(y0 - 1000*(a));
        line( img, pt1, pt2, Scalar(255,255,0),1);
    }

    imshow("source", img);
	waitKey(0);
    //imshow("detected lines", cdst);
	namedWindow("disp",WINDOW_NORMAL);
	waitKey(33);
	imwrite("output.jpg",th);
	imshow("disp",th);
	waitKey(0);
}

int main()
{
	
	getImage();
	return 0;
}


