using UnityEngine;
using UnityEngine.InputSystem;
using TMPro;
using UnityEngine.EventSystems;

public class BaristaInteraction : MonoBehaviour
{
    public GameObject dialogueCanvas;

    public InputActionReference interactAction;
    public InputActionReference cancelAction;

    public PlayerInput playerInput;
    public TMP_InputField playerInputField;

    private bool playerInRange = false;
    private bool dialogueOpen = false;

    void OnEnable()
    {
        interactAction.action.Enable();
        cancelAction.action.Enable();

        interactAction.action.performed += OnInteract;
        cancelAction.action.performed += OnCancel;
    }

    void OnDisable()
    {
        interactAction.action.performed -= OnInteract;
        cancelAction.action.performed -= OnCancel;

        interactAction.action.Disable();
        cancelAction.action.Disable();
    }

    private void OnInteract(InputAction.CallbackContext context)
    {
        if (playerInRange && !dialogueOpen)
        {
            dialogueCanvas.SetActive(true);
            dialogueOpen = true;

            playerInput.enabled = false;

            playerInputField.text = "";
            // Auto focus input field
            playerInputField.Select();
            playerInputField.ActivateInputField();
        }
    }

    private void OnCancel(InputAction.CallbackContext context)
    {
        if (dialogueOpen)
        {
            dialogueCanvas.SetActive(false);
            dialogueOpen = false;

            playerInput.enabled = true;    // allow movement again
        }
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Player"))
            playerInRange = true;
    }

    void OnTriggerExit2D(Collider2D other)
    {
        if (other.CompareTag("Player"))
            playerInRange = false;
    }
}