<template>
  <el-upload
    class="image-uploader-warp"
    :action="action"
    :headers="headers"
    :multiple="multiple"
    :data="data"
    :name="name"
    :with-credentials="withCredentials"
    :show-file-list="showFileList"
    :drag="drag"
    :accept="accept"
    :on-preview="onPreview"
    :on-success="onSuccess"
    :on-remove="onRemove"
    :before-upload="beforeUpload">
    <div class="el-upload-icon">
      <slot></slot>
    </div>
  </el-upload>
</template>
<script type="text/javascript">
  export default{
    props: {
      action: {
        type: String,
        require: true
      },
      headers: {
        type: Object
      },
      multiple: {
        type: Boolean,
        default: false
      },
      data: {
        type: Object
      },
      name: {
        type: String,
        default: 'file'
      },
      withCredentials: {
        type: Boolean,
        default: false
      },
      showFileList: {
        type: Boolean,
        default: false
      },
      drag: {
        type: Boolean,
        default: false
      },
      accept: {
        type: String
      },
      onPreview: {
        type: Function
      },
      onSuccess: {
        type: Function
      },
      onRemove: {
        type: Function
      },
      beforeUpload: {
        type: Function
      }
    },
    data(){
      return {
        upload_file: null
      }
    }
  }
</script>
<style lang="scss" type="text/scss" rel="stylesheet/scss">
  .image-uploader-warp {
    background-color: #fff;
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    box-sizing: border-box;
    width: 360px;
    height: 180px;
    text-align: center;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    &:hover {
      border-color: #20a0ff;
    }
    .el-upload {
      width: 100%;
      height: 100%;
    }
    .el-upload-icon {
      width: 100%;
      height: 100%;
    }
    img {
      position: absolute;
      left: 50%;
      top: 50%;
      max-width: none !important;
      transform: translate3d(-50%, -50%, 0);
    }
    [class*=" el-icon-"], [class^=el-icon-] {
      font-size: 67px;
      color: #97a8be;
      margin: 40px 0 16px;
      line-height: 50px;
    }
    .el-upload__text {
      color: #97a8be;
      font-size: 14px;
      text-align: center;
      em {
        color: #20a0ff;
        font-style: normal;
      }
    }
  }
</style>
