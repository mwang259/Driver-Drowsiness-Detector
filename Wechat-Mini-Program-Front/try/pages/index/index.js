//Mengyuan Wang 300256068
//Yufei Wang 300217244

// creating page
Page({

//the initial data of this page
 data: {
    tempFilePaths:'',
    resultdata:"Please click the button to start the detection"
  },

//loading the page
  onLoad: function () {   
    console.log("onLoad"); 
    this.setHeader();
},

// setting the function of clicking the photo and the action sheet 
    buttonclick: function () {
        const that = this
        wx.showActionSheet({
        itemList: ['album'],

//setting the function of action sheet
        success: function (res) {
            if (!res.cancel) {
            that.chooseImage(res)
            }
        }
        })
    },

// Setting the function of start button
    button: function () {
                var num =0
                console.log(111);
                wx.request({
                            url: 'http://127.0.0.1:5000/upload',//Server function address
                            method: "POST", // the method of get data 
                            header: {'content-type': "application/x-www-form-urlencoded",},
                            data: {image:num},
                            success: function (res) {
                                console.log(res.data);  //Return data
                            }
                        })
            },

//setting the path of file and get the picture; if not, showing the original photo of this system
    setHeader(){
        const tempFilePaths = wx.getStorageSync('tempFilePaths');
        if (tempFilePaths) {
            this.setData({
                tempFilePaths: tempFilePaths
            })
        } else {
            this.setData({
                tempFilePaths: '/images/original.png'
            })
        }
    },

// define the value of choosing picture
    chooseImage() {
        const that = this
        wx.chooseImage({
            //the count of choosing picture once time
            count: 1,
            success(res) {
                // tempFilePath can display pictures as the src attribute of the img tag
                console.log(res);
                const tempFilePaths = res.tempFilePaths
                //Cache the selected image in local storage
                wx.setStorageSync('tempFilePaths', tempFilePaths)
                //Using setHeader() method to update the avatar on the page
                that.setHeader();

            }
        })
    }
})