import os
import uuid
from flask import current_app, url_for
from werkzeug.utils import secure_filename
import logging

logger = logging.getLogger(__name__)

def allowed_file(filename, allowed_extensions):
    """检查文件扩展名是否允许上传
    
    Args:
        filename: 文件名
        allowed_extensions: 允许的文件扩展名列表
        
    Returns:
        bool: 如果文件扩展名在允许列表中返回True，否则返回False
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_file_info(file_path):
    """获取文件信息
    
    Args:
        file_path: 文件的完整路径
        
    Returns:
        dict: 包含文件信息的字典
    """
    if not os.path.exists(file_path):
        return None
        
    stat = os.stat(file_path)
    return {
        'size': stat.st_size,
        'created': stat.st_ctime,
        'modified': stat.st_mtime,
        'filename': os.path.basename(file_path)
    }

def delete_file(file_path):
    """删除文件
    
    Args:
        file_path: 文件的完整路径
        
    Returns:
        bool: 删除成功返回True，否则返回False
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"文件已删除: {file_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"删除文件失败: {str(e)}")
        return False

def save_file(file, folder_type):
    """
    保存上传的文件并返回URL路径
    
    Args:
        file: FileStorage对象
        folder_type: 文件类型 ('resumes', 'avatars', 'certificates')
        
    Returns:
        tuple: (存储路径, 访问URL) 或 (None, None)
    """
    if not file:
        logger.warning("没有文件被上传")
        return None, None
    
    # 获取配置
    if folder_type == 'resumes':
        upload_folder = current_app.config['RESUME_FOLDER']
        url_prefix = current_app.config['RESUME_URL_PREFIX']
        allowed_extensions = current_app.config['ALLOWED_RESUME_EXTENSIONS']
    elif folder_type == 'avatars':
        upload_folder = current_app.config['AVATAR_FOLDER']
        url_prefix = current_app.config['AVATAR_URL_PREFIX']
        allowed_extensions = current_app.config['ALLOWED_IMAGE_EXTENSIONS']
    else:  # certificates
        upload_folder = current_app.config['CERTIFICATE_FOLDER']
        url_prefix = current_app.config['CERTIFICATE_URL_PREFIX']
        allowed_extensions = current_app.config['ALLOWED_CERTIFICATE_EXTENSIONS']
    
    # 检查文件类型
    if not allowed_file(file.filename, allowed_extensions):
        logger.warning(f"不允许的文件类型: {file.filename}")
        return None, None
    
    # 确保目录存在
    os.makedirs(upload_folder, exist_ok=True)
    logger.info(f"上传目录: {upload_folder}")
    
    # 生成安全的文件名
    filename = secure_filename(file.filename)
    unique_filename = f"{str(uuid.uuid4())}_{filename}"
    file_path = os.path.join(upload_folder, unique_filename)
    
    try:
        file.save(file_path)
        file_info = get_file_info(file_path)
        logger.info(f"文件已保存: {file_path}")
        logger.info(f"文件信息: 大小={file_info['size']}字节")
        
        # 构建URL路径
        url_path = f"{url_prefix}/{unique_filename}"
        logger.info(f"访问URL: {url_path}")
        
        return file_path, url_path
    except Exception as e:
        logger.error(f"保存文件失败: {str(e)}")
        return None, None 