using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using TMPro;
using UnityEngine.InputSystem;
using Unity.Cinemachine;

[System.Serializable]
public class ChatRequest
{
    public string player_text;
}

public class NPCChat : MonoBehaviour
{
    public TMP_InputField playerInput;
    public TMP_Text npcText;
    public Transform outsideSpawn;
    public GameObject notificationCanvas;
    public TMP_Text notificationText;
    public GameObject dialogueCanvas;
    [SerializeField] PolygonCollider2D outsideBounds;


    string apiURL = "http://127.0.0.1:8000/chat";

    public void SendMessage()
    {
        StartCoroutine(SendChat());
    }

    IEnumerator SendChat()
    {
        string playerText = playerInput.text;

        // Show thinking indicator
        npcText.text = "...";
        playerInput.text = "";

        ChatRequest req = new ChatRequest();
        req.player_text = playerText;

        string json = JsonUtility.ToJson(req);

        UnityWebRequest request = new UnityWebRequest(apiURL, "POST");
        byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(json);

        request.uploadHandler = new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");

        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
        {
            string response = request.downloadHandler.text;

            ChatResponse chat = JsonUtility.FromJson<ChatResponse>(response);

            npcText.text = chat.reply;

            if (chat.consequence == "locked_out")
            {
                GameState.cafeBanned = true;
                HandleBan();
            }

        }
        else
        {
            npcText.text = "Something went wrong.";
            Debug.LogError(request.error);
        }

        playerInput.ActivateInputField();
    }

    void Update()
    {
        if (playerInput.isFocused)
        {
            if (Keyboard.current.enterKey.wasPressedThisFrame)
            {
                if (Keyboard.current.shiftKey.isPressed)
                {
                    // SHIFT + ENTER ? new line
                    playerInput.text += "\n";
                    playerInput.caretPosition = playerInput.text.Length;
                }
                else
                {
                    // ENTER ? send message
                    SendMessage();
                }
            }
        }
    }

    public void HandleSubmit(string text)
    {
        if (Keyboard.current.enterKey.wasPressedThisFrame &&
            !Keyboard.current.shiftKey.isPressed)
        {
            SendMessage();
        }
    }

    void LockOutPlayer()
    {
        GameObject player = GameObject.FindGameObjectWithTag("Player");

        player.transform.position = outsideSpawn.position;

        GameState.cafeBanned = true;

        dialogueCanvas.SetActive(false);

        CinemachineConfiner2D confiner = FindAnyObjectByType<CinemachineConfiner2D>();
        confiner.BoundingShape2D = outsideBounds;
    }

    IEnumerator ShowNotification(string message)
    {
        notificationCanvas.SetActive(true);
        notificationText.text = message;

        yield return new WaitForSeconds(5f);

        notificationCanvas.SetActive(false);

        Debug.Log("Showing ban notification");
    }

    void HandleBan()
    {
        GameObject player = GameObject.FindGameObjectWithTag("Player");

        if (player != null)
        {
            player.transform.position = outsideSpawn.position;

            CinemachineConfiner2D confiner = FindAnyObjectByType<CinemachineConfiner2D>();
            if (confiner != null)
            {
                confiner.BoundingShape2D = outsideBounds;
                confiner.InvalidateBoundingShapeCache();
            }

            PlayerInput playerInput = player.GetComponent<PlayerInput>();

            if (playerInput != null)
            {
                playerInput.enabled = true;
                playerInput.SwitchCurrentActionMap("Player");
            }
        }

        dialogueCanvas.SetActive(false);

        StartCoroutine(ShowNotification("You are banned from this cafe."));
    }
}

[System.Serializable]
public class ChatResponse
{
    public string reply;
    public int rating;
    public string consequence;
}