# Deployment Guide for Render.com

## Environment Variables to Set on Render.com

When deploying to Render.com, you need to set the following environment variables in your service settings:

### Required Environment Variables

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `OPENAI_API_KEY` | `your_actual_openai_api_key_here` | Your OpenAI API key from https://platform.openai.com/api-keys |
| `OPENAI_ASSISTANT_ID` | `your_actual_assistant_id_here` | Your OpenAI Assistant ID from https://platform.openai.com/assistants |

### Streamlit Configuration for Production

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `STREAMLIT_SERVER_PORT` | `10000` | Default port for Render.com web services |
| `STREAMLIT_SERVER_ADDRESS` | `0.0.0.0` | Allow external connections |
| `STREAMLIT_SERVER_HEADLESS` | `true` | Run without browser |
| `STREAMLIT_BROWSER_GATHER_USAGE_STATS` | `false` | Disable usage stats |
| `STREAMLIT_SERVER_ENABLE_CORS` | `false` | Disable CORS (handled by Render) |
| `STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION` | `false` | Disable XSRF protection |

### Python Configuration

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `PYTHON_VERSION` | `3.11.0` | Python version to use |

## Render.com Deployment Steps

### 1. Create Web Service
1. Go to [Render.com Dashboard](https://dashboard.render.com/)
2. Click "New" → "Web Service"
3. Connect your GitHub repository: `https://github.com/wxmbbr/botframe_for_Homepage`

### 2. Configure Service Settings
- **Name**: `bbr-chatbot` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: Leave empty (uses root)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run app_streamlit_render.py --server.port=$PORT --server.address=0.0.0.0`

### 3. Set Environment Variables
In the "Environment" section, add all the variables from the table above with your actual values.

### 4. Deploy
Click "Create Web Service" and Render will automatically deploy your app.

## Important Notes

### Port Configuration
- Render.com automatically provides a `$PORT` environment variable
- The start command uses `$PORT` which Render sets to the appropriate port
- Don't hardcode port numbers in the start command

### SSL/HTTPS
- Render.com automatically provides SSL certificates
- Your app will be available at: `https://your-service-name.onrender.com`

### Custom Domain (Optional)
- You can add a custom domain in the service settings
- Update DNS records as instructed by Render

### File Structure Considerations
- The `config.py` file is not uploaded to GitHub (excluded by .gitignore)
- The app reads from environment variables as fallback
- Make sure your `app_streamlit_v2.py` handles environment variables properly

## Troubleshooting

### Build Fails
- Check that `requirements.txt` includes all dependencies
- Verify Python version compatibility

### App Won't Start
- Check the logs in Render dashboard
- Ensure all environment variables are set correctly
- Verify the start command syntax

### API Connection Issues
- Double-check your OpenAI API key is valid
- Ensure your OpenAI account has sufficient credits
- Verify the Assistant ID is correct

### Performance Issues
- Consider upgrading to a paid Render plan for better performance
- Free tier has limitations on CPU and memory

## Cost Considerations

### Free Tier
- Render.com offers a free tier with limitations
- Apps may sleep after inactivity
- Limited bandwidth and compute resources

### Paid Plans
- For production use, consider paid plans
- Better performance and no sleep mode
- Custom domains and SSL included

## Security Best Practices

1. **Never commit API keys** to the repository
2. **Use environment variables** for all sensitive data
3. **Regularly rotate API keys**
4. **Monitor usage** in OpenAI dashboard
5. **Set up billing alerts** to avoid unexpected charges

## Alternative Deployment Options

If Render.com doesn't meet your needs, consider:
- **Streamlit Cloud**: Native Streamlit hosting
- **Heroku**: Popular PaaS platform
- **Railway**: Modern deployment platform
- **Google Cloud Run**: Serverless container platform
- **AWS ECS/Fargate**: Amazon container services

## Support

For deployment issues:
- Check Render.com documentation
- Review the logs in Render dashboard
- Ensure all environment variables match exactly
- Test locally first with the same environment variables
